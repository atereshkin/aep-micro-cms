# -*- coding: utf-8 -*-
from google.appengine.ext import db
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.template import loader, Context
from django.conf import settings

from dbtemplates.models import DbTemplate

class PageStorage(db.Expando):
    ''' Storage for editable information. '''

class Page(db.Model):
    """
    A page in CMS. All editable fragments are stored as
    fields with respecitve names in PageStorage instance
    corresponding to each instance.
    """
    title       = db.StringProperty()
    slug        = db.StringProperty()
    template    = db.ReferenceProperty(DbTemplate)
    parent_page = db.SelfReferenceProperty(default=None)
    order       = db.FloatProperty(default=1000.0)

    storage     = db.ReferenceProperty(PageStorage)
    
    def get_absolute_url(self):
        if self.parent_page:
            return "%s%s/" % (self.parent_page.get_absolute_url(),
                              self.slug)
        else:
            return reverse('cms_page', args=[self.slug])
                       
    
    def next_sibling(self):
        try:
            return Page.all().filter("parent_page =", self.parent_page).filter("order >", self.order)[0]
        except:
            return None

    def previous_sibling(self):
        try:
            return Page.all().filter("parent_page =", self.parent_page).filter("order <", self.order)[0]
        except:
            return None
        
    def children(self):
        return Page.all().filter("parent_page =", self).order("order")


    def __repr__(self):
        return "<Page: %s>" % self.slug

def get_template(template_name):
    ''' Returns django.template.Template instance with fully builded syntax
        tree.
    '''

    template = loader.get_template(template_name)

    # DO NOT DELETE
    # Needed for django to build full syntax tree of template
    try:
        template.render(Context({}))
    except:
        pass

    return template

def create_storage(sender, instance, **kwargs):
    ''' Creates a storage instance for all created instances of Page class.
        It's triggered on pre_save instead of post_save to avoid second
        save action.
    '''
    created = not instance.is_saved()

    if created and instance.storage is None:
        storage = PageStorage()
        storage.put()

        instance.storage = storage

def update_plugin_points(sender, instance, **kwargs):
    from django.templatetags.cms_tags import EditableNode

    template = get_template(instance.template.name)

    for node in walk(template):
        if isinstance(node, EditableNode):
            PluginPoint.get_or_insert(PluginPoint.keyname(instance, node.name),
                                      parent=instance,
                                      page=instance,
                                      name=node.name)

def update_plugin_points_template(sender, instance, created, **kwargs):
    ''' Updates plugin points of all the pages that use this particular
        template.
    '''
    from django.templatetags.cms_tags import EditableNode

    # doing nothing if template has just been created
    if created:
        return

    template = get_template(instance.name)
    pages = Page.all().filter('template =', instance)

    for node in walk(template):
        if isinstance(node, EditableNode):
            for page in pages:
                PluginPoint.get_or_insert(PluginPoint.keyname(page, node.name),
                                          parent=page,
                                          page=page,
                                          name=node.name)

    
def walk(node):
    yield node
    if hasattr(node, 'nodelist'):
        for subnode in node.nodelist:
            for subsub in walk(subnode):
                yield subsub
        
        

pre_save.connect(create_storage, sender=Page)                
post_save.connect(update_plugin_points, sender=Page)
post_save.connect(update_plugin_points_template, sender=DbTemplate)

class PluginPoint(db.Model):
    page        = db.ReferenceProperty(Page)
    name        = db.StringProperty()
    plugin_name = db.StringProperty(choices=settings.CMS_PLUGINS)
    content     = db.TextProperty()

    @staticmethod
    def keyname(page, name):
        return "pp_%s_%s" % (name, page.key())

    @staticmethod
    def get_by_address(page, name):
        return PluginPoint.get(PluginPoint.keyname(page,name))

    def __repr__(self):
        return self.name


    
