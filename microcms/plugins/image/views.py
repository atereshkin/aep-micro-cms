from django.http import HttpResponse
from google.appengine.ext import db

from ragendja.dbutils import get_object_or_404

from microcms.models import Page
from microcms.plugins.image.models import Image
from microcms.plugins.image import ImagePlugin

def upload_image(request, page_key, plugin_name):
    """
    A view for Ajax image upload.
    """
    page = get_object_or_404(Page, page_key)
    if request.method == "POST":
        img = Image()
        img.data = request.FILES['value'].read()
        img.put()
        setattr(page, plugin_name, img.key())
        page.put()
    plugin = ImagePlugin(plugin_name, page)
    return HttpResponse(plugin.render())


def render_image(request, image_key):
    """
    Serves image data. 
    """
    img = get_object_or_404(Image, image_key)
    #TODO[Alex Tereshkin|2009-09-23]: mime types
    return HttpResponse(img.data)
