from django import template
register = template.Library()

@register.filter(name='key')
def key(d, key_name):
    if not d: return ''
    try:
        value = d[key_name]
    except KeyError:
        return None
    return value
