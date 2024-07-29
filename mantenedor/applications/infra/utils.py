from django.contrib import messages
from decimal import Decimal, InvalidOperation

def parse_int(value, field_name):
    try:
        return int(value.strip())
    except ValueError:
        raise ValueError(f"El tipo de dato recibido en el campo '{field_name}' no es un entero válido: '{value}'")

def parse_decimal(value, field_name):
    try:
        return Decimal(value)
    except (ValueError, InvalidOperation) as e:
        raise ValueError(f"El tipo de dato recibido en el campo {field_name} no es un valor válido: '{value}'")    

def msg_error(request, view, form, message):
    messages.error(request, message)
    return view.form_invalid(form)

def validar_mes(mes):
    if mes < 1 or mes > 12:
        raise ValueError(f"El número del mes '{mes}' no es válido debe estar entre 1 y 12.")

def validar_dia(dia):
    if dia < 1 or dia > 31:
        raise ValueError(f"El número del dia '{dia}' no es válido debe estar entre 1 y 31.")

def validar_hora(hora):
    if hora < 0 or hora > 23:
        raise ValueError(f"El número de hora '{hora}' no es válido debe estar entre 0 y 23.")        