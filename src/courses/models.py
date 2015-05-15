from django.db import models
# Create your models here.
from datetime import date
import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from accounts.models import User


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
        super(Course, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):        
        self.full_clean()
        super(Course, self).save(*args, **kwargs)

    def Is_enrollment_open(self):
        return self.Is_always_open or (date.today() <= self.Enrollment_due_date)

    def Is_ongoing(self):
        return date.today() <= self.End_date

    def enroll(self, user_id):
        print self.id, user_id
        user = User.objects.get(id=user_id)
        e = Enrolled(course=self, student=user)
        e.save()


class Enrolled(models.Model):

    student = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    date_joined = models.DateField(editable=False, auto_now_add=True)

    class Meta:
        verbose_name = "Enrolled"
        verbose_name_plural = "2-Enrolled"


class Assignment(models.Model):

    Course = models.ForeignKey(Course)

    Title = models.CharField('Title', max_length=50)
    Creation_date = models.DateField(editable=False, auto_now_add=True)
    Activation_date = models.DateField()  # date after the Assignment will be available
    Due_date = models.DateField()
    Hard_date = models.DateField()
    Has_due_date = models.BooleanField()  # ignore due date if false
    Penality_percent = models.IntegerField()  # penality if complete after the due date

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "3-Assignments"

    def __str__(self):
        return '%s_%s' % (self.id, self.Title)


class Test(models.Model):

    Assignment = models.ForeignKey(Assignment)

    Creation_date = models.DateField(editable=False, auto_now_add=True)
    Number = models.IntegerField()  # cardinal of test
    File_to_complete = models.FilePathField()
    File_to_test = models.FilePathField()
    Points = models.IntegerField()

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "4-Tests"

    def __str__(self):
        return '%s #-%s' % (self.Assignment, self.Number)


class Result(models.Model):

    Test = models.ForeignKey(Test)
    User = models.ForeignKey(User, limit_choices_to={'is_staff': False})
    Creation_date = models.DateField(editable=False, auto_now_add=True)
    Update_date = models.DateField(editable=False, blank=True)

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "5-Results"

    def __str__(self):
        return '%s - %s' % (self.Test, self.User)
