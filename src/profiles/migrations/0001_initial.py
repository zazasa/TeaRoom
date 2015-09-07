# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('slug', models.SlugField(unique=True, max_length=32, editable=False, blank=True)),
                ('picture', models.ImageField(upload_to='profile_pics/%Y-%m-%d/', null=True, verbose_name='Profile picture', blank=True)),
                ('bio', models.CharField(max_length=200, null=True, verbose_name='Short Bio', blank=True)),
                ('email_verified', models.BooleanField(default=False, verbose_name='Email verified')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
