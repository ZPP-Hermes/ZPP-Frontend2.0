from django.db import models


class Subject(models.Model):
    code = models.CharField(max_length=250,
                            verbose_name='The USOS code of a subject')
    name = models.CharField(max_length=250,
                            verbose_name='The name of the subject')


class Semester(models.Model):
    code = models.CharField(max_length=250,
                            verbose_name='The USOS code of a semester')
    period = models.CharField(max_length=250,
                            verbose_name='Period of which the semester object represents')
    period_start = models.DateField(verbose_name='The physical start date of the Semester')
    period_end = models.DateField(verbose_name='The physical end date of the Semester')


class SubjectInstance(models.Model):
    type = models.ForeignKey('Subject',
                             blank=False,
                             null=False,
                             verbose_name='Subject')
    semester = models.ForeignKey('Semester',
                                 blank=False,
                                 null=False,
                                 verbose_name='The semester when the subject will be taught')
    coordinator = models.ManyToManyField('Person',
                                         verbose_name='The subject\'s coordinator')


class Person(models.Model):
    usos_id = models.CharField(max_length=250,
                            verbose_name='The USOS id of a person')
    first_name = models.CharField(max_length=250,
                            verbose_name='Person\'s first name')
    last_name = models.CharField(max_length=250,
                            verbose_name='Person\'s last name')


class SubjectParticipant(models.Model):
    person = models.ForeignKey('Person',
                               blank=False,
                               null=False,
                               verbose_name='The person that this entry represents')
    is_student = models.BooleanField(default=True,
                                     verbose_name='Whether this person is a student')


class Group(models.Model):
    usos_id = models.CharField(max_length=250,
                            verbose_name='The USOS id of a group')
    subject = models.ForeignKey('SubjectInstance',
                                blank=False,
                                null=False,
                                verbose_name='The subject instance of this group')
    participants = models.ManyToManyField('SubjectParticipant',
                                          verbose_name='The participants of this group, students/coordinators')


class Grade(models.Model):
    participant = models.ForeignKey('SubjectParticipant',
                                    blank=False,
                                    null=False,
                                    verbose_name='The student to which the grade is assigned')
    subject = models.ForeignKey('SubjectInstance',
                                blank=False,
                                null=False,
                                verbose_name='The subject which is the target of grading')
    grade_first = models.IntegerField(verbose_name='The grade on the first term')
    grade_second = models.IntegerField(verbose_name='The grade on the second term')


class StudyingProgram(models.Model):
    code = models.CharField(max_length=250,
                            verbose_name='The USOS code of a program')
    students = models.ManyToManyField('Person',
                                      verbose_name='Students which are part of this program')


class ObligatorySubject(models.Model):
    subject = models.ForeignKey('Subject',
                                blank=False,
                                null=False,
                                verbose_name='The subject beeing represented')
    program = models.ForeignKey('StudyingProgram',
                                blank=False,
                                null=False,
                                verbose_name='The program which this entry represents')
