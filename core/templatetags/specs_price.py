from django import template

register = template.Library()


@register.filter
def calcprice(tag):
    tag = tag / 100
    return tag


@register.filter
def get_total(items):
    total = 0
    for item in items:
        total += item.price
    return "$" + str(total / 100)
