from django.contrib import admin
from .models import DbTemplate

class TemplateAdmin(admin.ModelAdmin):
    pass

admin.site.register(DbTemplate, TemplateAdmin)
