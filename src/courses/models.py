from django.db import models
# Create your models here.


class Course(models.Model):
    Name = models.CharField('Course Name', max_length=50)
    Year = models.IntegerField()
    Creation_date = models.DateField()
    Start_date = models.DateField()
    End_date = models.DateField()
    Enrollment_due_date = models.DateField()
    Is_always_open = models.BooleanField()  # Ignore Enrollment_due_date
    Is_ongoing = models.BooleanField()
    Is_always_active = models.BooleanField()  # Ignore End_date
    Description = models.TextField()

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return "%s %s" % (self.Name, str(self.Year))
        