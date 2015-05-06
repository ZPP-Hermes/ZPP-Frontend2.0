"""
Definition of models.
"""

from django.db import models

class TermDim(models.Model):
    PERIODS = (
        ('L', 'Zimowy'),
        ('Z', 'Letni'),
    )
    term = models.CharField(max_length=250, choices=PERIODS)
    year = models.PositiveSmallIntegerField()

class CourseDim(models.Model):
    TYPES = (
        ('SEM_MGR', 'Seminarium magisterskie'),
        ('SEM_MONO', 'Seminarium monograficzne'),
        ('SEM_LIC', 'Seminarium licencjackie'),
        ('OBOW', 'Przedmiot obowiazkowy'),
        ('OBIER_ST', 'Przedmiot obieralny staly'),
        ('OBIER', 'Przedmiot obieralny'),
        ('FUND', 'Przedmiot fundamentalny'),
        ('FAKULT', 'Przedmiot fakultatywny'),
        ('MONO', 'Przedmiot monograficzny')
    )
    PROGRAMS = (
        ('DZ_MAT', 'Matematyka 1 stopnia'),
        ('DZ_INF', 'Informatyka 1 stopnia'),
        ('DZ_BIOINF', 'Bioinformatyka 1 stopnia'),
        ('S2_MAT', 'Matematyka 2 stopnia'),
        ('S2_INF', 'Informatyka 2 stopnia'),
        ('S2_BIOINF', 'Bioinformatyka 2 stopnia')
    )
    name = models.CharField(max_length=250)
    program = models.CharField(max_length=250, choices=PROGRAMS)
    type = models.CharField(max_length=250, choices=TYPES)

class MarkDim(models.Model):
    MARKS = (
        (4, '2'),
        (6, '3'),
        (7, '3.5'),
        (8, '4'),
        (9, '4.5'),
        (10, '5'),
        (11, '5!')
    )
    mark = models.IntegerField(default=6, choices=MARKS)

class StudentDim(models.Model):
    usos_id = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)

class InstructorDim(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    affiliation = models.CharField(max_length=250)
    institute = models.CharField(max_length=250)

class CourseTypeDim(models.Model):
    TYPES = (
        ('WYK', 'Seminarium'),
        ('LAB', 'Laboratorium'),
        ('CW', 'Cwiczenia'),
        ('SEM', 'Seminarium')
    )
    type = models.CharField(max_length=250, choices=TYPES)

class GroupNumberDim(models.Model):
    number = models.IntegerField()

class StudentMarksFact(models.Model):
    term = models.ForeignKey('TermDim', blank=False, null=False) 
    student = models.ForeignKey('StudentDim', blank=False, null=False)
    instructor = models.ForeignKey('InstructorDim', blank=False, null=False)
    mark = models.ForeignKey('MarkDim', blank=False, null=False)
    course = models.ForeignKey('CourseDim', blank=False, null=False)
    count = models.IntegerField(default=1)

class StudentGroupsFact(models.Model):
    term = models.ForeignKey('TermDim', blank=False, null=False) 
    student = models.ForeignKey('StudentDim', blank=False, null=False)
    instructor = models.ForeignKey('InstructorDim', blank=False, null=False)
    course = models.ForeignKey('CourseDim', blank=False, null=False)
    course_type = models.ForeignKey('CourseTypeDim', blank=False, null=False)
    number = models.ForeignKey('GroupNumberDim', blank=False, null=False)
    count = models.IntegerField(default=1)



