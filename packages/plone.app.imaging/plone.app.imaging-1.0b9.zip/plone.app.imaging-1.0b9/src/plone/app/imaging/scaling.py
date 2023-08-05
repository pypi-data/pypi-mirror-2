from logging import exception
from Acquisition import aq_base
from ZODB.POSException import ConflictError
from zope.interface import implements
from zope.traversing.interfaces import ITraversable, TraversalError
from zope.publisher.interfaces import IPublishTraverse, NotFound
from plone.app.imaging.interfaces import IImageScaling, IImageScaleFactory
from plone.app.imaging.scale import ImageScale
from plone.scale.storage import AnnotationStorage
from plone.scale.scale import scaleImage
from Products.Five import BrowserView


class ImageScaleFactory(object):
    """ adapter for image fields that allows generating scaled images """
    implements(IImageScaleFactory)

    def __init__(self, field):
        self.field = field

    def create(self, context, **parameters):
        value = self.field.get(context)
        data = getattr(aq_base(value), 'data', value)
        if data:
            return scaleImage(data, **parameters)


class ImageScaling(BrowserView):
    """ view used for generating (and storing) image scales """
    implements(IImageScaling, ITraversable, IPublishTraverse)

    def publishTraverse(self, request, name):
        """ used for traversal via publisher, i.e. when using as a url """
        stack = request.get('TraversalRequestNameStack')
        if stack:
            # field and scale name were given...
            scale = stack.pop()
            image = self.scale(name, scale)             # this is aq-wrapped
        elif '.' in name:
            # we got a uid...
            uid, ext = name.rsplit('.', 1)
            storage = AnnotationStorage(self.context)
            info = storage.get(uid)
            if info is not None:
                image = self.make(info).__of__(self.context)
        else:
            # otherwise `name` must refer to a field...
            field = self.field(name)
            image = field.get(self.context)             # this is aq-wrapped
        if image is not None:
            return image
        raise NotFound(self, name, self.request)

    def traverse(self, name, furtherPath):
        """ used for path traversal, i.e. in zope page templates """
        if not furtherPath:
            field = self.context.getField(name)
            return field.get(self.context).tag()
        image = self.scale(name, furtherPath.pop())
        if image is not None:
            return image.tag()
        raise TraversalError(self, name)

    def make(self, info):
        """ instantiate an object implementing `IImageScale` """
        mimetype = info['mimetype']
        info['content_type'] = mimetype
        info['filename'] = self.context.getFilename()
        scale = ImageScale(info['uid'], **info)
        scale.size = len(scale.data)
        url = self.context.absolute_url()
        extension = mimetype.split('/')[-1]
        scale.url = '%s/@@images/%s.%s' % (url, info['uid'], extension)
        return scale

    def field(self, fieldname):
        """ return the field for a given name """
        if fieldname:
            return self.context.getField(fieldname)
        else:
            return self.context.getPrimaryField()

    def create(self, fieldname, direction='keep', **parameters):
        """ factory for image scales, see `IImageScaleStorage.scale` """
        field = self.field(fieldname)
        create = IImageScaleFactory(field).create
        try:
            return create(self.context, direction=direction, **parameters)
        except (ConflictError, KeyboardInterrupt):
            raise
        except Exception:
            if not field.swallowResizeExceptions:
                raise
            else:
                exception('could not scale "%r" of %r',
                    field, self.context.absolute_url())

    def modified(self):
        """ provide a callable to return the modification time of content
            items, so stored image scales can be invalidated """
        return self.context.modified().millis()

    def scale(self, fieldname=None, scale=None, **parameters):
        if scale is not None:
            field = self.field(fieldname)
            available = field.getAvailableSizes(self.context)
            if not scale in available:
                return None
            width, height = available[scale]
            parameters.update(width=width, height=height)
        storage = AnnotationStorage(self.context, self.modified)
        info = storage.scale(factory=self.create,
            fieldname=fieldname, **parameters)
        if info is not None:
            return self.make(info).__of__(self.context)
