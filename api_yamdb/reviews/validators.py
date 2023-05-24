import datetime as dt
import re

from rest_framework import serializers


def validate_name(value):
    if value == 'me':
        raise serializers.ValidationError(
            "Это имя использовать запрещено!"
        )
    # if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
    #     raise serializers.ValidationError(
    #         f'Недопустимые символы <{value}> в имени пользователя.'
    #     )
    result = re.sub('([\w.@+-]+)', '', value)
    result_set = set(result)
    if len(result_set) != 0:
        raise serializers.ValidationError(
            f'Недопустимые символы {result_set} в имени пользователя.'
        )
    return value


def validate_year_field(value):
    if value > dt.date.today().year:
        raise serializers.ValidationError(
            "Год выпуска произведения не может быть больше текущего.")
    return value


def validate_genre_field(value):
    if not value:
        raise serializers.ValidationError("Не заполнено поле жанр.")
    return value