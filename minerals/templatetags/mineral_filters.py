import re
from django import template

register = template.Library()


@register.filter(name='base_name')
def base_name(string):
    """
    Removes suffixes and returns single base mineral name, leaving hyphenated
    names intact.
    ("Agardite-(Y)" will become "Agardite", but "Fluor-uvite" is unchanged.)
    """
    pattern = r'^[\w-]+[\w]'
    match = re.match(pattern, string)
    if match:
        return match[0]
    else:
        return string
