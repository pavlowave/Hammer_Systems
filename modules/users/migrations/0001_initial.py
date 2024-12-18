# Generated by Django 5.1.3 on 2024-11-30 16:49

import django.db.models.deletion
import modules.users.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone_number', models.CharField(help_text='Номер телефона пользователя в формате +7XXXXXXXXXX. Должен быть уникальным.', max_length=15, unique=True)),
                ('invite_code', models.CharField(default=modules.users.models.generate_invite_code, help_text='Уникальный инвайт-код, генерируется автоматически.', max_length=6, unique=True)),
                ('invited_by', models.ForeignKey(blank=True, help_text='Пользователь, который пригласил данного пользователя. Может быть пустым.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invited_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
