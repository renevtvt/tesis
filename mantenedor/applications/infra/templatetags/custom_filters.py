from django import template

register = template.Library()

@register.filter
def intcomma_custom(value):
    # Aplica intcomma para obtener el formato estándar
    formatted_value = "{:,.0f}".format(value)
    # Reemplaza la coma por un punto si es necesario (ajustado para es-cl)
    return formatted_value.replace(',', '.')