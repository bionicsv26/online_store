from django import template


register = template.Library()


@register.filter()
def format_array(list_prices: list) -> str:
    if len(list_prices) > 1:
        return f"{min(list_prices)} - {max(list_prices)}"
    else:
        return f"{min(list_prices)}"
