from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from braces.views import LoginRequiredMixin
# Create your views here.
from .models import *


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "course_list.html"