from django import template
from django.contrib.staticfiles import finders
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def template_exists(value: str) -> bool:
    """Returns a boolean value indicating whether or not a template exists

    Args:
        value (str): The file path to a template

    Returns:
        bool: True if the template exists, False otherwise
    """

    try:
        template.loader.get_template(value)
        return True
    except template.TemplateDoesNotExist:
        return False


@register.filter
def get_item(dictionary: dict, key):
    """Returns an item in a dictionary based on a key

    Args:
        dictionary (dict): The dictionary from which to get the item
        key: The dictionary key

    Returns:
        The item from the dictionary that matches the key
    """
    return dictionary.get(key)
