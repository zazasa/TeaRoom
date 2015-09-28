from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from os.path import join, isdir, dirname
from os import path, makedirs, listdir, walk, remove
from django.contrib.auth import authenticate
from shutil import rmtree, copytree
import time
import tarfile
import subprocess
import sys
import pickle
from courses.models import Course, Assignment, Exercise, UserFile, Result
from py_compile import compile
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datetime import datetime, date
import binascii
from django.http import HttpResponse, HttpResponseNotFound
import traceback
from subprocess import Popen, PIPE, STDOUT
from braces.views import LoginRequiredMixin, CsrfExemptMixin, StaffuserRequiredMixin
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
class UtilsView(LoginRequiredMixin, StaffuserRequiredMixin, TemplateView):
    template_name = "utils.html"


class DownloadUtilsFileView(LoginRequiredMixin, StaffuserRequiredMixin, View):
    def get_assignment_uploader(self):
        original_file = join(settings.USER_DATA_ROOT, 'utils/assignment_uploader.py')
        print original_file
        with open(original_file, 'rb') as original: data = original.read()
        data = "SSL_CERT_URL = \"%s\" \n" % str(settings.SSL_CERT_URL) + data
        data = "BASE_URL = \"%s\" \n" % str(settings.SITE_URL) + data
        return data

    def get(self, request, *args, **kwargs):
        try:
            file_requested = request.GET.get('file') or False
            if file_requested == "assignment_uploader":
                file_to_send = self.get_assignment_uploader()
                response = HttpResponse(file_to_send, content_type="text/plain")
                response['Content-Disposition'] = 'attachment; filename=assignment_uploader.py'
                return response
            else:
                raise
        except:
            return HttpResponseNotFound('Utils file not found or malformed.')


class UploadAssignmentView(TemplateView):
    template_name = "upload_assignment.txt"
    content_type = 'text/plain'
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
            except Exception:
                messages.error(self.request, self.messages['generic_error'] % traceback.format_exc())
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
        # assignment_number = settings['ASSIGNMENT_NUMBER']
        uniqueString = settings['ASSIGNMENT_TITLE'].strip().upper()
        c = Course.objects.get(id=course_id)
        if not c:
            raise Exception('Course with id %s does not exist.' % (course_id))
        try:
            a = Assignment.objects.get(Course=c, UniqueString=uniqueString)
            messages.info(self.request, 'Assigment already exists. Updating.')
        except:
            messages.info(self.request, 'Assigment does not exists. Creating.')
            a = Assignment(Course=c, Title=settings['ASSIGNMENT_TITLE'])
        a.Title = settings['ASSIGNMENT_TITLE']
        activation_date = settings['ACTIVATION_DATE']
        hard_date = settings['HARD_DATE']
        if ('DUE_DATE' in settings.keys()):
            due_date = settings['DUE_DATE']
        else:
            due_date = False

        if ('PENALTY_PERCENT' in settings.keys()):
            penalty_percent = settings['PENALTY_PERCENT']
        else:
            penalty_percent = 0

        if not penalty_percent:
            penalty_percent = 0

        if activation_date:
            a.Activation_date = activation_date

        if hard_date:
            a.Hard_date = hard_date
            a.Due_date = hard_date
            a.Penalty_percent = penalty_percent

        if due_date:
            a.Due_date = due_date
            a.Penalty_percent = penalty_percent
        a.save()
        return a

    def parse_exercises_settings(self, a, ex_settings, temp_folder):
        for ex_setting in ex_settings:
            ordinal_number = ex_setting['ORDINAL_NUMBER']
            try:
                # Update pre-existing exercise
                e = Exercise.objects.get(Assignment=a, Number=ordinal_number)
                messages.info(self.request, 'Exercise %s already exists. Updating.' % str(e.id))
            except:
                # Exercise does not exist: create it

                e = Exercise(Assignment=a, Number=ordinal_number)
                messages.info(self.request, 'Exercise %s doesnt exists. Creating.' % str(e.Description))

            e.Description = ex_setting['SHORT_DESCRIPTION']
            e.Points = ex_setting['POINTS']
            e.Group = ex_setting['GROUP']
            e.save()

            exercise_folder = str(e.Folder_path)
            dest_user_files = join(settings.USER_DATA_ROOT, exercise_folder, 'user_files')
            dest_test_files = join(settings.USER_DATA_ROOT, exercise_folder, 'test_files')

            # Remove files from disk
            old_package = None
            try:
                old_package = UserFile.objects.get(Exercise=e, Type='package')
                remove(join(settings.USER_DATA_ROOT, str(old_package)))
            except MultipleObjectsReturned as exc:
                raise Exception(exc)
            except:
                print "Unhandled error"
                pass

            if isdir(dest_user_files): rmtree(dest_user_files)
            if isdir(dest_test_files): rmtree(dest_test_files)
            e.remove_all_files()  # Remove all files form the database

            copytree(join(temp_folder, ex_setting['RELATIVE_FOLDER'], 'user_files'), dest_user_files)
            copytree(join(temp_folder, ex_setting['RELATIVE_FOLDER'], 'test_files'), dest_test_files)

            e.update_file(ex_setting['FILE_TO_TEST'], 'to_test')
            e.update_file(ex_setting['OUTPUT_PARSER'], 'parser')
            #  Compile test file
            test_file = join(dest_test_files, ex_setting['FILE_TO_TEST'])
            compile(test_file, test_file + 'c', doraise=True)
            for filename in ex_setting['FILES_TO_COMPLETE']: e.update_file(filename, 'to_complete')

            self.build_submit_script(e, dest_user_files)
            package_name = a.Title.replace(' ', '_') + '.tar.gz'
            self.create_user_package(e, dest_user_files, exercise_folder, package_name)

    def build_submit_script(self, e, dest_user_files):
        file_list = [item.Name for item in e.userfile_set.filter(Type='to_complete')]
        original_file = join(settings.USER_DATA_ROOT, 'utils/submit.py')
        destination_file = join(dest_user_files, 'submit.py')
        with open(original_file, 'rb') as original: data = original.read()
        with open(destination_file, 'wb') as modified:
            data = "SSL_CERT_URL = \"%s\" \n" % str(settings.SSL_CERT_URL) + data
            data = "BASE_URL = \"%s\" \n" % str(settings.SITE_URL) + data
            data = "EXERCISE_ID = %s \n" % str(e.id) + data
            data = "FILES_TO_COMPLETE = %s \n" % str(file_list) + data
            data = "SUBMIT_KEY = %s \n" % str(int(binascii.hexlify(str(e.Submit_key)), 16)) + data
            modified.write(data)
        compile(destination_file, doraise=True)
        remove(destination_file)

    def create_user_package(self, e, dest_user_files, ex_folder, package_name):
        # Save to disk
        package_file = join(settings.USER_DATA_ROOT, ex_folder, package_name)
        make_tarfile(package_file, dest_user_files, package_name.replace('.tar.gz', ''))
        # Write into the database
        uf = UserFile(Exercise=e, Name=package_name, Folder_path=ex_folder, Type='package')
        uf.save()


def make_tarfile(output_filename, source_dir, folder_name):
    with tarfile.open(output_filename, "w:gz") as tar:
        # tar.add(source_dir, arcname=path.basename(source_dir))
        tar.add(source_dir, arcname=folder_name)


def save_uploaded_file(f, filepath):
        with open(filepath, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)


def copy_and_unzip(f, dest_folder):
    if not isdir(dest_folder): makedirs(dest_folder)
    filepath = join(dirname(dest_folder), f.name)
    save_uploaded_file(f, filepath)
    tfile = tarfile.open(filepath, 'r:gz')
    tfile.extractall(dest_folder)


# Create your views here.
class UploadResultView(TemplateView):
    template_name = "upload_result.txt"
    content_type = 'text/plain'
    messages = {
        'notexist': 'Submit file malformed. Please contact admins. Errorcode: %s',
        'generic_error': 'exception: %s',
        'auth_error': 'User or password invalid',
        'success': 'Result submit successful',
        'result': 'Exercise result: %s',
        'timedelta': 'Please wait 10 min from last submit. ',
        'hard_date': 'Sorry, too late, this exercise is expired in date: %s. ',
        'due_date': 'You submitted out of due date. This exercise will be valuated at %s % '
    }

    def authenticate(self):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            return user
        else:
            return False

    def check_submit_key(self, e, submit_key):
        try:
            submit_key = binascii.unhexlify(str(hex(int(submit_key)))[2:-1])
            assert(submit_key == str(e.Submit_key))
        except:
            raise ObjectDoesNotExist('Wrong submit key.')

    def download_test_file(self, e):
        userfile = e.userfile_set.get(Type='to_test')
        filename = userfile.Name
        filepath = str(userfile)
        filepath = join(settings.USER_DATA_ROOT, filepath)
        # You got the zip! Now, return it!
        
        response = HttpResponse(open(filepath, 'rb'), content_type='application/x-bytecode.python')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

    # def check_submit_delay(self, e):
    def check_submit_delay(self, e, user):
        # res_set = e.result_set.all().order_by('-Creation_date')
        res_set = e.result_set.filter(User=user).order_by('-Creation_date')
        if res_set:
            r = res_set[0]
            deltamin = (datetime.utcnow().replace(tzinfo=r.Creation_date.tzinfo) - r.Creation_date).seconds / 60
            if deltamin < 10:
                return False
        return True

    def check_hard_date(self, e):
        now = timezone.now()
        if e.Assignment.Hard_date <= now:
            return False
        return True

    def check_due_date(self, e):
        now = timezone.now()
        if e.Assignment.has_due_date() and e.Assignment.Due_date <= now:
            return False
        return True

    def parse_and_submit(self, e, user, different_user):
        f = self.request.FILES['file']
        res_folder = self.create_result_folder(user, e)
        copy_and_unzip(f, join(res_folder, 'user_files'))

        passed, out = self.execute_parser(e, res_folder)
        r = Result(Exercise=e, User=different_user or user, Pass=passed, Parser_output=out, Submit_by=user)
        r.save()
        return out

    def post(self, request):
        user = self.authenticate()
        if user:
            ex_id = self.request.POST.get('ex_id')
            req_type = self.request.POST.get('type')
            submit_key = self.request.POST.get('submit_key')
            different_user = self.request.POST.get('different_user') or False
            try:
                if user.is_staff:
                    e = Exercise.objects.get(id=ex_id)
                    if req_type == 'download':
                        return self.download_test_file(e)
                else:
                    e = user.exercise_set.get(id=ex_id)
                print e

                if different_user:
                    if not user.is_staff: raise Exception('Not a staff user')
                    different_user = User.objects.get(email=different_user)
                    self.check_submit_key(e, submit_key)

                    out = self.parse_and_submit(e, user, different_user)

                    messages.info(self.request, self.messages['success'])
                    messages.info(self.request, self.messages['result'] % out)

                elif not self.check_submit_delay(e, user):
                    messages.info(self.request, self.messages['timedelta'])
                elif not self.check_hard_date(e):
                    messages.info(self.request, self.messages['hard_date'] % e.Assignment.Hard_date)
                else:
                    if req_type == 'download':
                        return self.download_test_file(e)
                    if user.is_staff: raise Exception('This is a staff user')
                    self.check_submit_key(e, submit_key)

                    out = self.parse_and_submit(e, user, different_user)

                    messages.info(self.request, self.messages['success'])
                    messages.info(self.request, self.messages['result'] % out)
                    if not self.check_due_date(e):
                        messages.info(self.request, self.messages['due_date'] % e.Assignment.Penalty_percent)
            except ObjectDoesNotExist as e:
                print ex_id
                messages.error(self.request, self.messages['notexist'] % repr(e))
            except Exception:
                messages.error(self.request, self.messages['generic_error'] % traceback.format_exc())

        else:
            messages.error(self.request, self.messages['auth_error'])

        return self.render_to_response(self.get_context_data())

    def execute_parser(self, e, res_folder):
    
        parser_file = join(settings.USER_DATA_ROOT, str(e.userfile_set.get(Type='parser')))
        parser_cwd = join(dirname(parser_file))
        output_file = join(res_folder, 'user_files/output.txt')
        p = Popen(['python', parser_file, output_file], stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=parser_cwd)
        # put the pyc in the stdin of the subprocess (exec test)
        out, err = p.communicate()
        passed = not p.returncode
        if err: return False, err
        return passed, out

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
