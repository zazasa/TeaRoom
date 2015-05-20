from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from os.path import join, isdir
from os import path, makedirs, listdir, walk
from django.contrib.auth import authenticate
from shutil import rmtree, copytree
import time
import tarfile
import subprocess
import sys
import pickle
from courses.models import Course, Assignment, Exercise, UserFile


# Create your views here.
class UploadAssignmentView(TemplateView):
    template_name = "upload_assignment.txt"
    messages = {
        'success': 'File upload successful.',
        'generic_error': 'exception: %s',
        'auth_error': 'User or password invalid'
    }

    def authenticate(self):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active and user.is_staff:
            return True
        else:
            return False

    def post(self, request):
        if self.authenticate():
            f = self.request.FILES['file']
            try:
                temp_folder = self.copy_and_unzip(f)
                # temp_subfolder = join(temp_folder, listdir(temp_folder)[0])
                r, d, f = walk(temp_folder).next()
                temp_subfolder = join(temp_folder, d[0])
                self.parse_temp_folder(temp_subfolder)
                rmtree(temp_folder)
                messages.info(self.request, self.messages['success'])
            except Exception as e:
                messages.error(self.request, self.messages['generic_error'] % repr(e))
        else:
            messages.error(self.request, self.messages['auth_error'])
        return self.render_to_response(self.get_context_data())

    def copy_and_unzip(self, f):
        temp_folder = join(settings.USER_DATA_ROOT, 'temp/temp' + str(int(time.time() * 100000)))
        i = 0
        while path.exists(temp_folder):
            i += 1
            temp_folder = join(settings.USER_DATA_ROOT, 'temp/tmp' + str(i + int(time.time() * 100000)))

        makedirs(temp_folder)
        filepath = join(temp_folder, f.name)
        self.save_uploaded_file(f, filepath)
        tfile = tarfile.open(filepath, 'r:gz')
        tfile.extractall(temp_folder)
        return temp_folder

    def save_uploaded_file(self, f, filepath):
        with open(filepath, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def parse_temp_folder(self, temp_folder):
        settings_file = join(temp_folder, 'settings.pkl')
        settings = pickle.load(open(settings_file, 'rb'))
        a = self.parse_assignment_settings(settings['ASSIGNMENT_SETTINGS'])
        self.parse_exercises_settings(a, settings['EX_SETTINGS'], temp_folder)

    def parse_assignment_settings(self, settings):
        course_id = settings['COURSE_ID']
        assignment_number = settings['ASSIGNMENT_NUMBER']
        c = Course.objects.get(id=course_id)
        if not c:
            raise Exception('Course with id %s doesnt exist.' % (course_id))
        try:
            a = Assignment.objects.get(Course=c, Number=assignment_number)
        except:
            a = Assignment(Course=c, Title=settings['ASSIGNMENT_TITLE'], Number=assignment_number, Has_due_date=False)
        a.Title = settings['ASSIGNMENT_TITLE']
        activation_date = settings['ACTIVATION_DATE']
        hard_date = settings['HARD_DATE']
        due_date = settings['DUE_DATE']
        penality_percent = settings['PENALITY_PERCENT']

        if activation_date:
            a.Activation_date = activation_date
        if due_date:
            a.Due_date = due_date
            if penality_percent:
                a.Penality_percent = penality_percent
        if hard_date:
            a.Hard_date = hard_date

        a.save()
        return a

    def parse_exercises_settings(self, a, settings, temp_folder):
        for ex_settings in settings:
            ordinal_number = ex_settings['ORDINAL_NUMBER']
            try:
                e = Exercise.objects.get(Assignment=a, Number=ordinal_number)
            except:
                e = Exercise(Assignment=a, Description=ex_settings['SHORT_DESCRIPTION'], Number=ordinal_number)
            e.Description = ex_settings['SHORT_DESCRIPTION']
            e.Points = ex_settings['POINTS']
            e.save()

            exercise_folder = e.Folder_path
            dest_user_files = join(exercise_folder, 'user_files')
            dest_test_files = join(exercise_folder, 'test_files')

            if isdir(dest_user_files):
                rmtree(dest_user_files)

            if isdir(dest_test_files):
                rmtree(dest_test_files)

            copytree(join(temp_folder, ex_settings['RELATIVE_FOLDER'], 'user_files'), dest_user_files)
            copytree(join(temp_folder, ex_settings['RELATIVE_FOLDER'], 'test_files'), dest_test_files)

            for filename in ex_settings['FILES_TO_COMPLETE']:
                e.update_file(filename, 'to_complete')
            for filename in ex_settings['FILES_TO_TEST']:
                e.update_file(filename, 'to_test')
