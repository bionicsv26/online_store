from django import template


register = template.Library()


@register.filter()
def mul_price(value, other):
    return '{:.2f}'.format(float(value) * other)
