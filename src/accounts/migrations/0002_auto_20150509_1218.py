# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(db_column=b'status', default=b'untreated', editable=False, choices=[(b'untreated', 'Untreated yet'), (b'accepted', 'Registration has accepted'), (b'rejected', 'Registration has rejected'), (b'registered', 'User is registered')], max_length=10, verbose_name='status'),
        ),
    ]
