#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-11 16:35:37
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-13 19:54:11

from django.contrib import admin
# Register your models here.
from .models import *


class CourseAdmin(admin.ModelAdmin):
    '''
        Admin View for Course
    '''

    list_display = ('course_full_name', 'Start_date', 'End_date',
                    'Enrollment_due_date')

    list_filter = []

    def course_full_name(self, obj):
        return obj.__str__()


class EnrolledAdmin(admin.ModelAdmin):
    '''
        Admin View for Enrolled
    '''
    list_display = ('course', 'student', 'date_joined')

    def __init__(self, *args, **kwargs):
        super(EnrolledAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

admin.site.register(Enrolled, EnrolledAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment)
admin.site.register(Test)
admin.site.register(Result)
