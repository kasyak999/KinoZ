import json
from django import template
import ast


register = template.Library()


@register.filter
def split(value):
    """Фильтр, который разделяет строку по запятой."""
    return value.split(', ')


@register.filter
def numeric(value):
    """Фильтр, который разделяет число по тысячам."""
    value = f"{value:,}".replace(',', ' ')
    return value


@register.filter
def json_to_list(value):
    """Преобразует строку JSON в список."""
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return []


@register.filter
def to_dict(value):
    """Фильтр преобразует строку в словарь"""
    try:
        result = ast.literal_eval(value)
        if isinstance(result, dict):
            return result.items()
    except (ValueError, SyntaxError):
        pass
    return []


@register.filter
def join_list(value, delimiter=", "):
    """
    Преобразует список в строку с указанным разделителем.
    Если значение не список, возвращает исходное значение.
    """
    if isinstance(value, list):
        return delimiter.join(str(item) for item in value)
    return value
