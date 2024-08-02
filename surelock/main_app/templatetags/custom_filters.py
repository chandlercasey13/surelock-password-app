from django import template

register = template.Library()

@register.filter
def repeat(value, times):
    try:
        times = int(times)
        return value * times
    except ValueError:
        return value  # In case of an error, return the value as is
