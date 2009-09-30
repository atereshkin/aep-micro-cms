# -*- coding: utf-8 -*-
from google.appengine.ext import db
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.template import loader, Context
from django.conf import settings

from dbtemplates.models import DbTemplate

class Page(db.Expando):
    """
    A page in CMS. All editable fragments are stored as
    fields with respecitve names in this entity (hence the
    Expando subclass)
    """
    title       = db.StringProperty()
    slug        = db.StringProperty()
    template    = db.ReferenceProperty(DbTemplate)
    parent_page = db.SelfReferenceProperty(default=None)
    order       = db.FloatProperty(default=1000.0)
    
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


def update_plugin_points(sender, instance, **kwargs):
    created = not instance.is_saved()

    if not created:
        before = Page.get(instance.key())
        if before.template == instance.template:
           return

    from django.templatetags.cms_tags import EditableNode
    template = loader.get_template(instance.template.name)
    try:
        template.render(Context({}))
    except:
        pass
    for node in walk(template):
        if isinstance(node, EditableNode):
            PluginPoint.get_or_insert(PluginPoint.keyname(instance, node.name),
                                      parent=instance,
                                      page=instance,
                                      name=node.name)


def walk(node):
    yield node
    if hasattr(node, 'nodelist'):
        for subnode in node.nodelist:
            for subsub in walk(subnode):
                yield subsub
        
        

pre_save.connect(update_plugin_points, sender=Page)

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


    
