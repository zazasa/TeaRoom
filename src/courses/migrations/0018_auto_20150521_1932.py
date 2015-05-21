# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_auto_20150521_1926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enrolled',
            old_name='course',
            new_name='Course',
        ),
        migrations.RenameField(
            model_name='enrolled',
            old_name='date_joined',
            new_name='Date_joined',
        ),
        migrations.RenameField(
            model_name='enrolled',
            old_name='student',
            new_name='Student',
        ),
    ]
