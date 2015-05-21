from django.shortcuts import render
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import ProcessFormView
from django.views.generic.base import TemplateResponseMixin, ContextMixin, TemplateView
from braces.views import LoginRequiredMixin, CsrfExemptMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings
# Create your views here.
from accounts.models import User
from .models import *


class CourseListView(LoginRequiredMixin, ListView):
    messages = {
        'invalid_enroll_id': 'Unable to find the course you want to enroll to. Please contact admins',
        'course_closed': 'Enrollments for this course are closed at this time.'
    }
    model = Course
    context_object_name = 'courses'
    template_name = "course_list.html"
    success_url = reverse_lazy('courses:course-list')

    show_other = False
    show_closed = False

    # custom queryset called by the listview, if getEnroll = False avoid to get enroll_id from request (used by post request).
    # Dont change the default due to the listview compatibility
    def get_queryset(self):
        self.show_other = self.request.GET.get('show_other') == 'True'
        self.show_closed = self.request.GET.get('show_closed') == 'True'
        
        if not self.show_closed:
            dataSet = self.model.objects.filter_ongoing()
        else:
            dataSet = self.model.objects.all()
        if not self.show_other:
            dataSet = dataSet.filter(Students=self.request.user)
        else:
            dataSet = dataSet.exclude(Students=self.request.user)
        return dataSet

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseListView, self).get_context_data(**kwargs)

        context['mycourses'] = self._get_mycourses(context['object_list'])
        context['show_other'] = self.show_other
        context['show_closed'] = self.show_closed
        return context

    def post(self, request):
        # enroll_id corresponds to the course id
        enroll_id = self.request.POST.get('enroll_id') or False
        enroll_id = self._clean_enroll_id(enroll_id)
        if not enroll_id:
            redirect_url = self.request.get_full_path()
            return HttpResponseRedirect(redirect_url)
        else:
            course = self.model.objects.get(id=enroll_id)
            course.enroll(self.request.user.id)
            return HttpResponseRedirect(self.success_url)

    def _clean_enroll_id(self, enroll_id):
        """
        Verify that a course with this ID exists and is open for enrollments
        """
        try:
            enroll_id = int(enroll_id)
            course = self.model.objects.get(id=enroll_id)
        except:
            course = False
        if not course:
            messages.error(self.request, self.messages['invalid_enroll_id'])
            return False
        if not course.Is_enrollment_open():
            messages.error(self.request, self.messages['course_closed'])
            return False
        return enroll_id

    # list of courses to which the user is enrolled
    def _get_mycourses(self, courses_list):
        mycourses = []
        for course in courses_list.filter(Students=self.request.user):
            mycourses.append(course.id)
        return mycourses


class AssignmentListView(LoginRequiredMixin, ListView):
    
    template_name = "assignment_list.html"
    context_object_name = 'courses'

    def get_queryset(self):
        courses_list = Course.objects.filter(Students=self.request.user)
        return courses_list

    def get_context_data(self, **kwargs):
        context = super(AssignmentListView, self).get_context_data(**kwargs)
        courses_list = context['courses']
        if courses_list:
            selected_course_id = self.request.GET.get('selected_course_id') or False
            if selected_course_id:
                try:
                    selected_course = courses_list.get(id=selected_course_id)
                except:
                    selected_course = courses_list[0]
            else:
                selected_course = courses_list[0]
            assignment_list = Assignment.objects.filter(Course=selected_course)
            exercise_list = self.request.user.exercise_set.all()
            print '>>>>>>>>>>>>>>>', exercise_list
            context['assignments'] = assignment_list
            context['exercises'] = exercise_list
            context['selected_course'] = selected_course

        return context
    
