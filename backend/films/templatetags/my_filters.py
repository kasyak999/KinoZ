import json
from django import template


register = template.Library()


@register.filter
def split(value: str):
    """Фильтр, создает список."""
    if value is None:
        return []
    return value.split(', ')


@register.filter
def numeric(value: int):
    """Фильтр, который разделяет число по тысячам."""
    return f"{value:,}".replace(',', ' ')


@register.filter
def json_to_list(value):
    """Преобразует строку JSON в список."""
    return json.loads(value)


@register.filter
def list_to_str(value: list):
    """Преобразует список в строку"""
    return ', '.join(value)
