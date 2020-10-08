import random
import string

from django.utils.text import slugify


def unique_slug(s: str, model, num_chars=50) -> str:
    """Return slug of num_chars length unique to model

    Args:
        s (str): The value to be slugified.
        model: The model to which the object belongs.
        num_chars (int, optional): The max length that the slug should be. Defaults to 50.

    Returns:
        str: A unique slug
    """

    slug = slugify(s)
    slug = slug[:num_chars].strip('-')
    while True:
        dup = model.objects.filter(slug=slug)
        if not dup:
            return slug

        slug = slug[:39] + '-' + random_string(10)


def random_string(num_chars=10) -> str:
    """Returns a random string of num_chars length

    Args:
        num_chars (int, optional): Length of the string. Defaults to 10.

    Returns:
        str: A random string of num_chars length
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(num_chars))
