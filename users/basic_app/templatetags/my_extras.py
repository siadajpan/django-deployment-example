from django import template

register = template.Library()


@register.filter(name="capital")
def all_capital(value: str):
    return value.capitalize()
