from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    usos_id = models.CharField(max_length=250)
    # models.OneToOneField('User', primary_key=True)
    #    courses=models.ManyToManyField(Course, through="Mark")
    def __unicode__(self):
        return self.usos_id


# models.OneToOneField('User', primary_key=True)
# courses=models.ManyToManyField(Course, through="Mark")

class Course(models.Model):
    TYPES = (
        ('OBOW', 'Przedmiot obowiazkowy'),
        ('OBIER', 'Przedmiot obieralny'),
        ('SEM', 'Seminarium')
    )
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250, choices=TYPES)
    url = models.CharField(max_length=250, null=True)
    mark4 = models.IntegerField()
    mark6 = models.IntegerField()
    mark7 = models.IntegerField()
    mark8 = models.IntegerField()
    mark9 = models.IntegerField()
    mark10 = models.IntegerField()
    mark11 = models.IntegerField()

    def __unicode__(self):
        return self.name


class Mark(models.Model):
    MARKS = (
        (4, '2'),
        (6, '3'),
        (7, '3+'),
        (8, '4'),
        (9, '4+'),
        (10, '5'),
        (11, '5!')
    )
    student = models.ForeignKey('Student', blank=False, null=False)
    course = models.ForeignKey('Course', blank=False, null=False)
    mark = models.IntegerField(max_length=250, choices=MARKS)


class SavedMark(models.Model):
    MARKS = (
        (4, '2'),
        (6, '3'),
        (7, '3+'),
        (8, '4'),
        (9, '4+'),
        (10, '5'),
        (11, '5!')
    )
    user = models.ForeignKey(User, blank=False, null=False)
    course = models.ForeignKey('Course', blank=False, null=False)
    mark = models.IntegerField(max_length=250, choices=MARKS)

    def __unicode__(self):
        return str(self.mark) + "__ " + self.course.url
