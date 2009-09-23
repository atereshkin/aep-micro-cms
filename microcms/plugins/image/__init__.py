from django.utils import simplejson
from django.core.urlresolvers import reverse

from microcms.plugins.base import SimplePlugin

class ImagePlugin(SimplePlugin):
    """
    Allows inserting images into the page. Renders as <img> tag.
    """
    def render(self):
        """
        See SimplePlugin.render
        """
        image_key = getattr(self.page, self.name, None)
        if image_key:
            return '<img src="%s" />' % reverse("cms_image",
                                                args=(str(image_key),))
        else:
            return "Edit Me"

    def save_url(self):
        """
        See SimplePlugin.save_url
        """
        return reverse("cms_upload_image", args=(str(self.page.key()),
                                                 self.name))
    
    def options(self):
        """
        See SimplePlugin.options
        """
        target = reverse("cms_upload_image", args=(str(self.page.key()),
                                                   self.name))
        return simplejson.dumps({ 'type' : 'ajaxupload',
                                  'submit' : 'OK',
                                  'cancel' : 'Cancel'})


