from django import template
from django.template.defaultfilters import stringfilter




register = template.Library()


@register.filter
@stringfilter
def replace_dash(value):
     
     value = value.replace("&nbsp;", " ")
     value = value.replace("&mdash;", "—")
     
     return value



