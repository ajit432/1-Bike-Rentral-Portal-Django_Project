from django import template
from datetime import datetime

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def days_between(date1, date2):
    """Calculate days between two dates."""
    try:
        if hasattr(date1, 'date'):
            date1 = date1.date()
        if hasattr(date2, 'date'):
            date2 = date2.date()
        
        delta = date2 - date1
        return delta.days
    except (TypeError, AttributeError):
        return 0
