from django.db import models
# Create your models here.
from datetime import date
import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from accounts.models import User
from os.path import join, isdir
from os import makedirs
from django.conf import settings
import random, string

class CourseManager(models.Manager):
    def filter_ongoing(self):
        return super(CourseManager, self).filter(End_date__gte=date.today())


class Course(models.Model):
    Name = models.CharField('Course Name', max_length=50)
    Year = models.IntegerField()
    Creation_date = models.DateField(editable=False, auto_now_add=True)
    Start_date = models.DateField()
    End_date = models.DateField()
    Enrollment_due_date = models.DateField()
    Is_always_open = models.BooleanField()  # Ignore Enrollment_due_date
    Is_always_active = models.BooleanField()  # Ignore End_date
    Description = models.TextField()
    Students = models.ManyToManyField(User, through='Enrolled')
    objects = CourseManager()
    Folder_path = models.CharField('Folder_path', max_length=200, null=True, blank=True, editable=False)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "1-Courses"
        unique_together = (("Name", "Year"),)

    def __str__(self):
        return "%s %s" % (self.Name, str(self.Year))

    def clean(self, *args, **kwargs):
        # add custom validation here
        if (self.Start_date > self.End_date):
            raise ValidationError('Start date cannot be greather than End_date')
        if (self.Enrollment_due_date > self.End_date):
            raise ValidationError('Enrollement due date cannot be greather than End_date')
        # call default cleaning
        super(Course, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Add cleaning before writing to DB (overriding django's default)
        """
        # check if the fields are correct before saving
        self.full_clean()
        # call default save
        
        course_folder = join('courses', str(self).replace(' ', '_'))
        self.Folder_path = course_folder
        
        super(Course, self).save(*args, **kwargs)
        # Create course folder in USER_DATA
        absolute_folder = join(settings.USER_DATA_ROOT, course_folder)
        if not isdir(absolute_folder):
            makedirs(absolute_folder)

    def Is_enrollment_open(self):
        return self.Is_always_open or (date.today() <= self.Enrollment_due_date)

    def Is_ongoing(self):
        return date.today() <= self.End_date

    def enroll(self, user_id):
        user = User.objects.get(id=user_id)
        e = Enrolled(Course=self, Student=user)
        e.save()


class Enrolled(models.Model):

    Student = models.ForeignKey(User)
    Course = models.ForeignKey(Course)
    Date_joined = models.DateField(editable=False, auto_now_add=True)

    class Meta:
        verbose_name = "Enrolled"
        verbose_name_plural = "2-Enrolled"
        unique_together = (("Student", "Course"),)


class Assignment(models.Model):

    Course = models.ForeignKey(Course)

    Number = models.IntegerField(null=True, blank=True)
    Title = models.CharField('Title', max_length=50)
    Creation_date = models.DateField(editable=False, auto_now_add=True)
    Activation_date = models.DateField(null=True, blank=True)  # date after the Assignment will be available
    Due_date = models.DateTimeField(null=True, blank=True)
    Hard_date = models.DateTimeField(null=True, blank=True)
    Has_due_date = models.BooleanField(default=False)  # ignore due date if false
    Penality_percent = models.IntegerField(null=True, blank=True)  # penality if complete after the due date
    Folder_path = models.CharField('Folder_path', max_length=200, null=True, blank=True, editable=False)

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "3-Assignments"
        unique_together = (("Course", "Number"),)

    def __str__(self):
        return '%s' % (self.Title)

    def clean(self, *args, **kwargs):
        # add custom validation here
        if self.Due_date:
            if not self.Penality_percent:
                raise ValidationError('Due date withouth penality percent')
            self.Has_due_date = True
        # call default cleaning
        super(Assignment, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        1 - Add cleaning before writing to DB (overriding django's default)
        2 - Create folder structure
        """
        # check if the fields are correct before saving
        self.full_clean()
        # call default save
        
        assignment_folder = join(self.Course.Folder_path, str(self).replace(' ', '_'))
        self.Folder_path = assignment_folder
        super(Assignment, self).save(*args, **kwargs)
        # Create course folder in USER_DATA
        absolute_folder = join(settings.USER_DATA_ROOT, assignment_folder)
        if not isdir(absolute_folder):
            makedirs(absolute_folder)


class Exercise(models.Model):

    Assignment = models.ForeignKey(Assignment)

    Description = models.CharField('Description', max_length=50, blank=True, null=True)
    Creation_date = models.DateField(editable=False, auto_now_add=True)
    Number = models.IntegerField()  # cardinal of test
    Points = models.IntegerField(blank=True, null=True)
    Folder_path = models.CharField('Folder_path', max_length=200, null=True, blank=True, editable=False)
    Students = models.ManyToManyField(User, through='Assigned')
    Submit_key = models.CharField('Submit key', max_length=25, editable=False)

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "4-Exercises"
        unique_together = (("Assignment", "Number"),)

    def __str__(self):
        return '%s - %s - %s' % (self.Assignment.Course, self.Assignment, self.Description)

    def save(self, *args, **kwargs):
        """
        1 - Add cleaning before writing to DB (overriding django's default)
        2 - Create folder structure
        """
        # check if the fields are correct before saving
        self.full_clean()
        # call default save
        
        exercise_folder = join(self.Assignment.Folder_path, 'ex_' + str(self.Number))
        self.Folder_path = exercise_folder
        self.Submit_key = ''.join(random.choice(string.letters + string.digits) for i in range(random.randint(15, 25)))
        super(Exercise, self).save(*args, **kwargs)
        # Create course folder in USER_DATA
        absolute_folder = join(settings.USER_DATA_ROOT, exercise_folder)
        if not isdir(absolute_folder):
            makedirs(absolute_folder)

    def update_file(self, name, ftype):
        try:
            f = UserFile.objects.get(Exercise=self, Name=name, Type=ftype)
        except:
            f = UserFile(Exercise=self, Name=name, Type=ftype)
            if ftype == 'to_complete':
                folder_path = join(self.Folder_path, 'user_files')
            elif ftype == 'to_test':
                folder_path = join(self.Folder_path, 'test_files')
            else:
                raise ValidationError('bad file type')
            f.Folder_path = folder_path
            f.save()

    def remove_all_files(self):
        UserFile.objects.filter(Exercise=self).delete()


class Assigned(models.Model):

    Student = models.ForeignKey(User)
    Exercise = models.ForeignKey(Exercise)
    Sate_assigned = models.DateField(editable=False, auto_now_add=True)
    Assigned_by = models.CharField('Assigned By', max_length=50, editable=False, blank=True, null=True)

    class Meta:
        verbose_name = "Assigned"
        verbose_name_plural = "5-Assigned"
        unique_together = (("Student", "Exercise"),)

    def clean(self, *args, **kwargs):
        # add custom validation here
        if not self.Student.enrolled_set.filter(Course=self.Exercise.Assignment.Course):
            raise ValidationError('The user %s is not enrolled in the course %s' % (self.Student, self.Exercise.Assignment.Course))
        # call default cleaning
        super(Assigned, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        1 - Add cleaning before writing to DB (overriding django's default)
        """
        # check if the fields are correct before saving
        self.full_clean()
        # call default save
        super(Assigned, self).save(*args, **kwargs)


class Result(models.Model):

    Exercise = models.ForeignKey(Exercise, null=True)

    User = models.ForeignKey(User, limit_choices_to={'is_staff': False})
    Creation_date = models.DateField(editable=False, auto_now_add=True)
    Update_date = models.DateField(editable=False, blank=True)
    Pass = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "6-Results"

    def __str__(self):
        return '%s - %s' % (self.Exercise, self.User)


class UserFile(models.Model):
    
    Exercise = models.ForeignKey(Exercise)

    Name = models.CharField('Filename', max_length=50)
    Folder_path = models.CharField('Folder_path', max_length=200, null=True, blank=True)
    Type = models.CharField('Type', max_length=50)  # to_complete or to_test

    class Meta:
        verbose_name = "UserFile"
        verbose_name_plural = "7-UserFiles"
        unique_together = (("Exercise", "Name"),)

    def __str__(self):
        return "%s" % join(self.Folder_path, self.Name)
    