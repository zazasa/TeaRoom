#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-11 17:31:12
# @Last Modified by:   salvo
# @Last Modified time: 2015-07-27 10:55:57

from django.conf.urls import patterns, url


from . import views
urlpatterns = patterns('',
                       url(r'^course-list/$', views.CourseListView.as_view(), name="course-list"),
                       url(r'^course-list-staff/$', views.CourseListStaffView.as_view(), name="course-list-staff"),
                       url(r'^assignment-list/$', views.AssignmentListView.as_view(), name="assignment-list"),
                       url(r'^assignment-list-staff/$', views.AssignmentListStaffView.as_view(), name="assignment-list-staff"),
                       url(r'^download-user-file/$', views.DownloadUserFileView.as_view(), name="download-user-file"),
                       url(r'^result-list/$', views.ResultListView.as_view(), name="result-list"),
                       )