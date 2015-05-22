from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from os.path import join, isdir
from os import path, makedirs, listdir, walk, remove
from django.contrib.auth import authenticate
from shutil import rmtree, copytree
import time
import tarfile
import subprocess
import sys
import pickle
from courses.models import Course, Assignment, Exercise, UserFile
from py_compile import compile
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


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
                temp_folder = join(settings.USER_DATA_ROOT, 'temp/temp' + str(int(time.time() * 100000)))
                copy_and_unzip(f, temp_folder)
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

    def parse_exercises_settings(self, a, ex_settings, temp_folder):
        for ex_setting in ex_settings:
            ordinal_number = ex_setting['ORDINAL_NUMBER']
            try:
                e = Exercise.objects.get(Assignment=a, Number=ordinal_number)
            except:
                e = Exercise(Assignment=a, Description=ex_setting['SHORT_DESCRIPTION'], Number=ordinal_number)
            e.Description = ex_setting['SHORT_DESCRIPTION']
            e.Points = ex_setting['POINTS']
            e.save()

            exercise_folder = str(e.Folder_path)
            dest_user_files = join(settings.USER_DATA_ROOT, exercise_folder, 'user_files')
            dest_test_files = join(settings.USER_DATA_ROOT, exercise_folder, 'test_files')

            if isdir(dest_user_files):
                rmtree(dest_user_files)

            if isdir(dest_test_files):
                rmtree(dest_test_files)

            copytree(join(temp_folder, ex_setting['RELATIVE_FOLDER'], 'user_files'), dest_user_files)
            copytree(join(temp_folder, ex_setting['RELATIVE_FOLDER'], 'test_files'), dest_test_files)

            for filename in ex_setting['FILES_TO_COMPLETE']:
                e.update_file(filename, 'to_complete')
            for filename in ex_setting['FILES_TO_TEST']:
                e.update_file(filename, 'to_test')

            file_to_complete_list = [item.Name for item in e.userfile_set.filter(Type='to_complete')]
            self.build_submit_script(e.id, file_to_complete_list, dest_user_files)
            self.create_user_package(dest_user_files, exercise_folder)

    def build_submit_script(self, ex_id, file_list, dest_user_files):
        original_file = join(settings.USER_DATA_ROOT, 'utils/submit.py')
        destination_file = join(dest_user_files, 'submit.py')
        with open(original_file, 'rb') as original: data = original.read()
        with open(destination_file, 'wb') as modified:
            data = "EXERCISE_ID = %s \n" % str(ex_id) + data
            data = "FILES_TO_COMPLETE = %s \n" % str(file_list) + data
            modified.write(data)
        compile(destination_file)
        remove(destination_file)

    def create_user_package(self, dest_user_files, ex_folder):
        package_file = join(settings.USER_DATA_ROOT, ex_folder, 'ex_package.tar.gz')
        make_tarfile(package_file, dest_user_files)


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=path.basename(source_dir))


def save_uploaded_file(f, filepath):
        with open(filepath, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)


def copy_and_unzip(f, dest_folder):
    if not isdir(dest_folder): makedirs(dest_folder)
    filepath = join(dest_folder, f.name)
    print 'XXXXXXXXX', filepath
    save_uploaded_file(f, filepath)
    tfile = tarfile.open(filepath, 'r:gz')
    tfile.extractall(dest_folder)


# Create your views here.
class UploadResultView(TemplateView):
    template_name = "upload_result.txt"
    messages = {
        'notexist': 'Bad exercise id. Please contact admins.',
        'generic_error': 'exception: %s',
        'auth_error': 'User or password invalid',
        'success': 'result submit successful',
    }

    def authenticate(self):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active and not user.is_staff:
            return user
        else:
            return False

    def post(self, request):
        user = self.authenticate()
        if user:
            ex_id = self.request.POST.get('ex_id')
            try:
                e = user.exercise_set.get(id=ex_id)
                f = self.request.FILES['file']
                res_folder = self.create_result_folder(user, e)
                print 'ZZZZZZZZZ ', res_folder
                copy_and_unzip(f, join(res_folder, 'user_files'))
                messages.info(self.request, self.messages['success'])
            except ObjectDoesNotExist:
                messages.error(self.request, self.messages['notexist'])
        #     try:
        #         temp_folder = join(settings.USER_DATA_ROOT, 'temp/temp' + str(int(time.time() * 100000)))
        #         copy_and_unzip(f, temp_folder)
        #         # temp_subfolder = join(temp_folder, listdir(temp_folder)[0])
        #         r, d, f = walk(temp_folder).next()
        #         temp_subfolder = join(temp_folder, d[0])
        #         self.parse_temp_folder(temp_subfolder)
        #         rmtree(temp_folder)
        #         messages.info(self.request, self.messages['success'])
            except Exception as e:
                messages.error(self.request, self.messages['generic_error'] % repr(e))

        else:
            messages.error(self.request, self.messages['auth_error'])

        return self.render_to_response(self.get_context_data())

    def create_result_folder(self, user, exercise):
        res_dest_folder = join(settings.USER_DATA_ROOT, str(exercise.Folder_path), 'RESULTS')
        user_dest_folder = join(res_dest_folder, str(user.name))
        timed_folder = join(user_dest_folder, 'result_' + str(datetime.now().isoformat().split('.')[0].replace(':', '_')))
        
        test_files = join(settings.USER_DATA_ROOT, str(exercise.Folder_path), 'test_files')
        user_files = join(settings.USER_DATA_ROOT, str(exercise.Folder_path), 'user_files')

        if not isdir(res_dest_folder): makedirs(res_dest_folder)
        if not isdir(user_dest_folder): makedirs(user_dest_folder)
        makedirs(timed_folder)  # this should not be overwritten

        copytree(test_files, join(timed_folder, 'test_files'))
        copytree(user_files, join(timed_folder, 'user_files'))

        return timed_folder





