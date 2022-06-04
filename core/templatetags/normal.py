from django import template

register = template.Library()


@register.filter
def removespace(tag):
    tag = tag.replace(" ", "-")
    return tag
