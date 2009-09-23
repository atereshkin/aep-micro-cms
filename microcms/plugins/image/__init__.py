from django.utils import simplejson
from django.core.urlresolvers import reverse

from microcms.plugins.base import SimplePlugin

class ImagePlugin(SimplePlugin):
    """
    Allows inserting images into the page. Renders as <img> tag.
    """
    def render(self):
        image_key = getattr(self.page, self.name, None)
        if image_key:
            return '<img src="%s" />' % reverse("cms_image",
                                                args=(str(image_key),))
        else:
            return "Edit Me"
    
    def options(self):
        target = reverse("cms_upload_image", args=(str(self.page.key()),
                                                   self.name))
        return simplejson.dumps({ 'type' : 'ajaxupload',
                                  'submit' : 'OK',
                                  'cancel' : 'Cancel',
                                  'target' : target})


