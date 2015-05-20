#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-11 16:35:37
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-20 14:50:41

from django.contrib import admin
# Register your models here.
from .models import *


class CourseAdmin(admin.ModelAdmin):
    '''
        Admin View for Course
    '''

    list_display = ('course_full_name', 'Start_date', 'End_date',
                    'Enrollment_due_date')
    readonly_fields = ('Folder_path',)
    list_filter = []

    def course_full_name(self, obj):
        return obj


class EnrolledAdmin(admin.ModelAdmin):
    '''
        Admin View for Enrolled
    '''
    list_display = ('course', 'student', 'date_joined')

    def __init__(self, *args, **kwargs):
        super(EnrolledAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )


class AssignmentAdmin(admin.ModelAdmin):
    '''
        Assignment View for Course
    '''

    list_display = ('Number', 'Title', 'Activation_date', 'Course')
    readonly_fields = ('Folder_path',)
    list_filter = []


class ExerciseAdmin(admin.ModelAdmin):
    '''
        Exercise View for Course
    '''

    list_display = ('Number', 'Description', 'Assignment', 'file_to_complete_list', 'file_to_test_list')
    readonly_fields = ('Folder_path',)

    list_filter = []

    def file_to_complete_list(self, obj):
        dataSet = UserFile.objects.filter(Exercise=obj, Type='to_complete')
        filelist = []
        for item in dataSet:
            filelist.append(item.Name)
        return ','.join(filelist)
    file_to_complete_list.short_description = 'To Complete'

    def file_to_test_list(self, obj):
        dataSet = UserFile.objects.filter(Exercise=obj, Type='to_test')
        filelist = []
        for item in dataSet:
            filelist.append(item.Name)
        return ','.join(filelist)
    file_to_test_list.short_description = 'To Test'
    

class UserFileAdmin(admin.ModelAdmin):
    '''
        Admin View for UserFile
    '''

    def __init__(self, *args, **kwargs):
        super(UserFileAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

admin.site.register(Enrolled, EnrolledAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Result)
admin.site.register(UserFile, UserFileAdmin)
