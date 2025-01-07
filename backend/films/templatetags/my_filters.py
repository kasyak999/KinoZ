import ast
import json
from django import template


register = template.Library()


@register.filter
def split(value):
    """Фильтр, создает список."""
    return value.split(', ')


@register.filter
def numeric(value):
    """Фильтр, который разделяет число по тысячам."""
    return f"{value:,}".replace(',', ' ')


@register.filter
def json_to_list(value):
    """Преобразует строку JSON в список."""
    return json.loads(value)


@register.filter
def str_to_dict(value):
    """Фильтр преобразует строку в словарь"""
    result = ast.literal_eval(value)
    return result.items()


@register.filter
def list_to_str(value):
    """Преобразует список в строку"""
    return str.join(', ', value)
