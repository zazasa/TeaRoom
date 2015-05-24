# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0020_auto_20150524_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='Update_date',
        ),
        migrations.AddField(
            model_name='result',
            name='Parser_output',
            field=models.TextField(default=b'', editable=False),
        ),
    ]
