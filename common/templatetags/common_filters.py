from django import template
from django.contrib.staticfiles import finders
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def template_exists(value):
    try:
        template.loader.get_template(value)
        return True
    except template.TemplateDoesNotExist:
        return False

@register.filter
@stringfilter
def static_file_exists(value):
    if finders.find(value) is None:
        return False
    else:
        return True