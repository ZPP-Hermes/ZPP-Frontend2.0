from django.contrib.auth.models import User
from django.db import models

# ###############################
# Student i Mark to w tej chwili zapamietane dane wprowadzone przez uzytkownika
# niezalezne od dumpa na ktorym bedziemy sie uczyc
# jesli dalej chcemy trzymac dumpa w bazie djangowej trzeba bedzie miec
# osobne instancje Student i Mark
#################################




class Course(models.Model):
    TYPES = (
        ('OBOW', 'Przedmiot obowiazkowy'),
        ('OBIER', 'Przedmiot obieralny'),
        ('SEM', 'Seminarium')
    )
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250, choices=TYPES)
    users = models.ManyToManyField(User, through="Mark")
    def __unicode__(self):
        return self.name

#class Student(models.Model):
#    usos_id = models.CharField(max_length=250)
#    models.OneToOneField('User', primary_key=True)
#    courses=models.ManyToManyField(Course, through="Mark")


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
    student = models.ForeignKey(User, blank=False, null=False)
    course = models.ForeignKey('Course', blank=False, null=False)
    mark = models.IntegerField(choices=MARKS)
    def __unicode__(self):
        return self.mark
