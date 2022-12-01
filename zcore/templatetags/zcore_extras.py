from django import template
register = template.Library()

import os

@register.filter
def env(key):
    return os.environ.get(key, "")