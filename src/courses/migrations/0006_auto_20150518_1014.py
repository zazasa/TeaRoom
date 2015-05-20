# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20150513_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Creation_date', models.DateField(auto_now_add=True)),
                ('Number', models.IntegerField()),
                ('Exercise_folder', models.FilePathField()),
                ('File_to_test', models.FilePathField()),
                ('Points', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Exercise',
                'verbose_name_plural': '4-Exercises',
            },
        ),
        migrations.RemoveField(
            model_name='test',
            name='Assignment',
        ),
        migrations.AlterModelOptions(
            name='assignment',
            options={'verbose_name': 'Assignment', 'verbose_name_plural': '3-Assignments'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Course', 'verbose_name_plural': '1-Courses'},
        ),
        migrations.AlterModelOptions(
            name='enrolled',
            options={'verbose_name': 'Enrolled', 'verbose_name_plural': '2-Enrolled'},
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'verbose_name': 'Result', 'verbose_name_plural': '5-Results'},
        ),
        migrations.RemoveField(
            model_name='result',
            name='Test',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='Due_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='Hard_date',
            field=models.DateTimeField(),
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AddField(
            model_name='exercise',
            name='Assignment',
            field=models.ForeignKey(to='courses.Assignment'),
        ),
        migrations.AddField(
            model_name='result',
            name='Exercise',
            field=models.ForeignKey(to='courses.Exercise', null=True),
        ),
    ]
