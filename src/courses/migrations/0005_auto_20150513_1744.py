# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0004_remove_course_is_ongoing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Title', models.CharField(max_length=50, verbose_name=b'Title')),
                ('Creation_date', models.DateField(auto_now_add=True)),
                ('Activation_date', models.DateField()),
                ('Due_date', models.DateField()),
                ('Hard_date', models.DateField()),
                ('Has_due_date', models.BooleanField()),
                ('Penality_percent', models.IntegerField()),
                ('Course', models.ForeignKey(to='courses.Course')),
            ],
            options={
                'verbose_name': 'Assignment',
                'verbose_name_plural': 'Assignments',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Creation_date', models.DateField(auto_now_add=True)),
                ('Update_date', models.DateField(editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Result',
                'verbose_name_plural': 'Results',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Creation_date', models.DateField(auto_now_add=True)),
                ('Number', models.IntegerField()),
                ('File_to_complete', models.FilePathField()),
                ('File_to_test', models.FilePathField()),
                ('Points', models.IntegerField()),
                ('Assignment', models.ForeignKey(to='courses.Assignment')),
            ],
            options={
                'verbose_name': 'Test',
                'verbose_name_plural': 'Tests',
            },
        ),
        migrations.AddField(
            model_name='result',
            name='Test',
            field=models.ForeignKey(to='courses.Test'),
        ),
        migrations.AddField(
            model_name='result',
            name='User',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
