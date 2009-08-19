# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('microcms.views',
    url(r'^(?P<path>.+)/$', 'show_page', name='cms_page'),
)
