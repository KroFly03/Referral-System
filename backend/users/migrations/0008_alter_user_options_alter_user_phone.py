# Generated by Django 4.2.4 on 2023-08-21 12:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_activated_invite_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='Номер телефона должен быть в формате: +7 (999) 123-45-67.', regex='^\\+7\\s\\(\\d{3}\\)\\s\\d{3}-\\d{2}-\\d{2}$')], verbose_name='Телефон'),
        ),
    ]
