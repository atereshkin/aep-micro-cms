from django.contrib import admin
from django.utils import simplejson
from django.core import urlresolvers
from django.http import HttpResponse
from django.conf.urls.defaults import *

from ragendja.dbutils import get_object_or_404

from microcms.models import Page, PluginPoint

class PluginPointInline(admin.StackedInline):
    model  = PluginPoint
    extra  = 0
    fields = ('plugin_name',)


def build_tree(root=None):
    if root:
        ret =  { 'attributes' : { 'id' : str(root.key()) },
                 'data' : { 'title' : root.title,
                            'attributes' : { 'class' : 'link',
                                             'href' : urlresolvers.reverse('admin_microcms_page_change', args=(root.id,))}},
                 }
        children = Page.all().filter("parent_page =", root)
        if children.count() > 0:
            ret['children'] = [build_tree(page) for page in children]
            ret['state'] = 'open'
        return ret
    
    else:
        return [build_tree(page) for page in Page.all().filter("parent_page =", None)]

class PageAdmin(admin.ModelAdmin):
    inlines = [PluginPointInline, ]
    
    def changelist_view(self, request, extra_context=None):
        return super(PageAdmin, self).changelist_view(request,
                                                      extra_context={'tree_json' : simplejson.dumps(build_tree())})


    def move(self, request):
        import logging
        logging.error(request.POST)
        page = get_object_or_404(Page, request.POST['page_id'])
        target = get_object_or_404(Page, request.POST['target_id'])
        if request.POST['position'] == 'inside':
            page.parent_page = target
        else:
            page.parent_page = target.parent_page
        page.put()
        
        return HttpResponse('ok')

    def get_urls(self):
        urls = super(PageAdmin, self).get_urls()
        upd_urls = patterns('',
            url(r'^move/$', self.move, name='admin_microcms_page_move')
        )
        return upd_urls + urls




admin.site.register(Page, PageAdmin)
