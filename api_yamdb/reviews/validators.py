import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """Валидация по году произведения."""
    if value > dt.date.today().year:
        raise ValidationError(
            f'Вносимый год еще не наступил, сейчас {dt.date.today().year}')
    return value
