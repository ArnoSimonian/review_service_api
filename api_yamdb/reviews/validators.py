import re

from rest_framework import serializers


def validate_name(value):
    if value == 'me':
        raise serializers.ValidationError(
            "Это имя использовать запрещено!"
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise serializers.ValidationError(
            f'Не допустимые символы <{value}> в имени пользователя.'
        )
    return value
