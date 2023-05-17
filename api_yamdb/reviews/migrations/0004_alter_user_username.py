# Generated by Django 3.2 on 2023-05-16 21:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Не соответствует регулярному выражению!', regex='^[\\w.@+-]+\\Z')], verbose_name='имя пользователя'),
        ),
    ]