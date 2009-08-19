from django.contrib import admin
from microcms.models import Page, PluginPoint


class PluginPointInline(admin.StackedInline):
    model  = PluginPoint
    extra  = 0
    fields = ('plugin_name',)

class PageAdmin(admin.ModelAdmin):
    inlines = [PluginPointInline, ]


admin.site.register(Page, PageAdmin)
