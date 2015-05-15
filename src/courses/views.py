from django.shortcuts import render
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import ProcessFormView
from django.views.generic.base import TemplateResponseMixin, ContextMixin, TemplateView
from braces.views import LoginRequiredMixin, CsrfExemptMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
# Create your views here.
from accounts.models import User
from . import models


class CourseListView(LoginRequiredMixin, ListView):
    messages = {
        'invalid_enroll_id': 'Unable to find the course you want to enroll to. Please contact admins',
        'course_closed': 'Enrollments for this course are closed at this time.'
    }
    model = models.Course
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
            dataSet = dataSet.filter(Students__id=self.request.user.id)
        else:
            dataSet = dataSet.exclude(Students__id=self.request.user.id)

        return dataSet

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseListView, self).get_context_data(**kwargs)

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
            course = self.model.objects.filter(id=enroll_id)
        except:
            course = False
        if not course:
            messages.error(self.request, self.messages['invalid_enroll_id'])
            return False
        if not course.Is_enrollment_open():
            messages.error(self.request, self.messages['course_closed'])
            return False
        return enroll_id


class HelpView(TemplateView):
    template_name = "help.html"
