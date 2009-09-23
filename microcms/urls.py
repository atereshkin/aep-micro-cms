# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('microcms.plugins.image.views',
    url(r'^images/upload/(?P<page_key>\w+)/(?P<plugin_name>\w+)/$', 'upload_image', name='cms_upload_image'),                       
    url(r'^images/(?P<image_key>\w+)/', 'render_image', name='cms_image'),                                             
)

urlpatterns += patterns('microcms.views',
    url(r'^(?P<path>.+)/$', 'show_page', name='cms_page'),
)
