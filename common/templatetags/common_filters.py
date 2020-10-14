from django import template
from django.contrib.staticfiles import finders
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def template_exists(path_to_template: str) -> bool:
    """Returns True if path_to_template exists."""

    try:
        template.loader.get_template(path_to_template)
        return True
    except template.TemplateDoesNotExist:
        return False


@register.filter
def get_item(dictionary: dict, key):
    """Returns the value for key in dictionary or None if key doesn't exist."""
    return dictionary.get(key)
