# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=50, verbose_name=b'Course Name')),
                ('Year', models.IntegerField()),
                ('Creation_date', models.DateField()),
                ('Start_date', models.DateField()),
                ('End_date', models.DateField()),
                ('Enrollment_due_date', models.DateField()),
                ('Is_always_open', models.BooleanField()),
                ('Is_ongoing', models.BooleanField()),
                ('Is_always_active', models.BooleanField()),
                ('Description', models.TextField()),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
    ]
