from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from microcms.models import Page, PluginPoint
from microcms.plugins.base import SimplePlugin

register = template.Library()

def do_editable(parser, token):
    error_string = '%r tag requires three arguments' % token.contents[0]
    try:
        # split_contents() knows not to split quoted strings.
        bits = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(error_string)
    if len(bits) == 2:
        #tag_name, name
        return EditableNode(bits[1])
    elif len(bits) == 3:
        #tag_name, name, container_name
        return EditableNode(bits[1], bits[2])
    else:
        raise template.TemplateSyntaxError(error_string)

class EditableNode(template.Node):
    def __init__(self, name, container_name="div"):
        self.name = name.lower()
        self.container_name = container_name

    def render(self, context):
        if not 'page' in context:
            return ''#render_to_string('cms/plugin.html')

        page = context['page']
        user = context.get('user', None)

        pp = page.pluginpoint_set.filter('name =', self.name)[0]
        dot = pp.plugin_name.rindex('.')
        plugin_module, plugin_classname = pp.plugin_name[:dot], pp.plugin_name[dot+1:]
        mod = __import__(plugin_module, {}, {}, [''])
        plugin_class = getattr(mod, plugin_classname)
        plugin = plugin_class(self.name, page)
        return render_to_string('cms/editable.html',
                                { 'tag'     : self.container_name,
                                  'id'      : self.name,
                                  'plugin'  : plugin,
                                  'user'    : user })
        
    def __repr__(self):
        return "<EditableNode: %s>" % self.name

register.tag('editable', do_editable)


def menu(context, template='cms/menu.html', page=None):
    pages = Page.all().filter("parent_page =", page)
    context.update( {'pages' : pages,
                     'template' : template})
    return context


register.inclusion_tag('cms/dummy.html', takes_context=True)(menu)
    

def menu_below(context, slug, template='cms/menu.html'):
    page = Page.all().filter("slug =", str(slug))[0]
    return menu(context, template, page)


register.inclusion_tag('cms/dummy.html', takes_context=True)(menu_below)
