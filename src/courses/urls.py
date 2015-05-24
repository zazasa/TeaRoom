#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-11 17:31:12
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-24 22:52:10

from django.conf.urls import patterns, url


from . import views
urlpatterns = patterns('',
                       url(r'^course-list/$', views.CourseListView.as_view(), name="course-list"),
                       url(r'^assignment-list/$', views.AssignmentListView.as_view(), name="assignment-list"),
                       url(r'^download-user-file/$', views.DownloadUserFileView.as_view(), name="download-user-file"),
                       url(r'^result-list/$', views.ResultListView.as_view(), name="result-list"),
                       )