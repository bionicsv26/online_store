from django import template

register = template.Library()


@register.simple_tag()
def get_current_radio_value(field):
    return dict(field.field.choices).get(field.value())
