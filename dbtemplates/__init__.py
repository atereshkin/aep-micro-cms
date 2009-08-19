from django.template import TemplateDoesNotExist

def db_loader(template_name, template_dirs=None):
    from .models import DbTemplate
    try:
        template = DbTemplate.all().filter("name =", template_name)[0]
        return (template.content, "db://%s"%template_name)
    except:
        raise TemplateDoesNotExist, template_name
db_loader.is_usable = True
