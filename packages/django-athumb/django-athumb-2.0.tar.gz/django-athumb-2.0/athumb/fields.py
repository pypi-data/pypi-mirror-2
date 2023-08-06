# -*- encoding: utf-8 -*-
"""
Fields, FieldFiles, and Validators.
"""
import os
import cStringIO
import re

from PIL import Image
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from django.conf import settings
from django.core.cache import cache

from manipulations import generate_thumb_basic, sorl_scale_and_crop
from validators import ImageUploadExtensionValidator

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^athumb\.fields\.ImageWithThumbsField"])
except ImportError:
    # Not using South, no big deal.
    pass

# Cache URLs for thumbnails so we don't have to keep re-generating them.
THUMBNAIL_URL_CACHE_TIME = getattr(settings, 'THUMBNAIL_URL_CACHE_TIME', 3600 * 24)

# Models want this instantiated ahead of time.
IMAGE_EXTENSION_VALIDATOR = ImageUploadExtensionValidator()

class ImageWithThumbsFieldFile(ImageFieldFile):
    """
    Serves as the file-level storage object for thumbnails.
    """
    def generate_url(self, thumb_name, ssl_mode=False):
        # This is tacked on to the end of the cache key to make sure SSL
        # URLs are stored separate from plain http.
        ssl_postfix = '_ssl' if ssl_mode else ''

        # Try to see if we can hit the cache instead of asking the storage
        # backend for the URL. This is particularly important for S3 backends.
        cache_key = "Thumbcache_%s_%s%s" % (self.url,
                                               thumb_name,
                                               ssl_postfix)

        cached_val = cache.get(cache_key)
        if cached_val:
            return cached_val

        # Determine what the filename would be for a thumb with these
        # dimensions, regardless of whether it actually exists.
        new_filename = self._calc_thumb_filename(thumb_name)

        # Split URL from GET attribs.
        url_get_split = self.url.rsplit('?', 1)
        # Just the URL string (no GET attribs).
        url_str = url_get_split[0]
        # Get the URL string without the original's filename at the end.
        url_minus_filename = url_str.rsplit('/', 1)[0]

        # Slap the new thumbnail filename on the end of the old URL, in place
        # of the orignal image's filename.
        new_url = "%s/%s?cbust=%s" % (url_minus_filename,
                                      os.path.basename(new_filename),
                                      settings.MEDIA_CACHE_BUSTER)

        if ssl_mode:
            new_url = new_url.replace('http://', 'https://')

        # Cache this so we don't have to hit the storage backend for a while.
        cache.set(cache_key, new_url, THUMBNAIL_URL_CACHE_TIME)
        return new_url

    def get_thumbnail_format(self):
        """
        Determines the target thumbnail type either by looking for a format
        override specified at the model level, or by using the format the
        user uploaded.
        """
        if self.field.thumbnail_format:
            # Over-ride was given, use that instead.
            return self.field.thumbnail_format.lower()
        else:
            # Use the existing extension from the file.
            filename_split = self.name.rsplit('.', 1)
            return filename_split[-1]

    def save(self, name, content, save=True):
        """
        Handles some extra logic to generate the thumbnails when the original
        file is uploaded.
        """
        super(ImageWithThumbsFieldFile, self).save(name, content, save)

        # see http://code.djangoproject.com/ticket/8222 for details
        content.seek(0)
        image = Image.open(content)

        # Convert to RGBA (alpha) if necessary
        if image.mode not in ('L', 'RGB', 'RGBA'):
            image = image.convert('RGBA')

        for thumb in self.field.thumbs:
            thumb_name, thumb_options = thumb
            # Pre-create all of the thumbnail sizes.
            self.create_and_store_thumb(image, thumb_name, thumb_options)

        #blah = getattr(self, 'url_%d_%d' % (100, 100))
        #print "BLAH", blah

    def _calc_thumb_filename(self, thumb_name):
        """
        Calculates the correct filename for a would-be (or potentially
        existing) thumbnail of the given size.
        
        NOTE: This includes the path leading up to the thumbnail. IE:
        uploads/cbid_images/photo.png
        
        size: (tuple) In the format of (width, height)
        
        Returns a string filename.
        """
        filename_split = self.name.rsplit('.', 1)
        file_name = filename_split[0]
        file_extension = self.get_thumbnail_format()

        return '%s_%s.%s' % (file_name, thumb_name, file_extension)

    def create_and_store_thumb(self, image, thumb_name, thumb_options):
        """
        Given that 'image' is a PIL Image object, create a thumbnail for the
        given size tuple and store it via the storage backend.
        
        image: (Image) PIL Image object.
        size: (tuple) Tuple in form of (width, height). Image will be
            thumbnailed to this size.
        """
        size = thumb_options['size']
        thumb_filename = self._calc_thumb_filename(thumb_name)
        file_extension = self.get_thumbnail_format()

        # The work starts here.
        thumb_content = sorl_scale_and_crop(image, thumb_options, file_extension)
        # Save the result to the storage backend.
        thumb_name_ = self.storage.save(thumb_filename, thumb_content)

        # Some back-ends don't like over-writing stuff. I guess. Not sure
        # if this is necessary.
        if not thumb_filename == thumb_name_:
            raise ValueError('There is already a file named %s' % thumb_filename)

    def delete(self, save=True):
        """
        Deletes the original, plus any thumbnails. Fails silently if there
        are errors deleting the thumbnails.
        """
        for thumb in self.field.thumbs:
            thumb_name, thumb_options = thumb
            thumb_filename = self._calc_thumb_filename(thumb_name)
            self.storage.delete(thumb_filename)

        super(ImageWithThumbsFieldFile, self).delete(save)

class ImageWithThumbsField(ImageField):
    """
    Usage example:
    ==============
    photo = ImageWithThumbsField(upload_to='images', thumbs=((125,125),(300,200),)
        
    Note: The 'thumbs' attribute is not required. If you don't provide it, 
    ImageWithThumbsField will act as a normal ImageField
    """
    attr_class = ImageWithThumbsFieldFile

    def __init__(self, *args, **kwargs):
        self.thumbs = kwargs.pop('thumbs', ())
        self.thumbnail_format = kwargs.pop('thumbnail_format', None)

        if not kwargs.has_key('validators'):
            kwargs['validators'] = [IMAGE_EXTENSION_VALIDATOR]
            
        if not kwargs.has_key('max_length'):
            kwargs['max_length'] = 255

        super(ImageWithThumbsField, self).__init__(*args, **kwargs)
