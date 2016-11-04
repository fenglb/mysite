from django import template
from django.template.defaultfilters import stringfilter
from mistune.markdown_mistune import markdown2html_mistune as md

register = template.Library()

@register.filter
@stringfilter
def markdown2html(text):
    return md(text)
