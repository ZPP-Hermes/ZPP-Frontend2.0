from django.db import models
 
# Create your models here.


class Student(models.Model):
	usos_id = models.CharField(max_length = 250)

class Course(models.Model):
	TYPES = (
		('OBOW', 'Przedmiot obowiazkowy'),
		('OBIER', 'Przedmiot obieralny'),
		('SEM', 'Seminarium')
	)
	name = models.CharField(max_length = 250)
	type = models.CharField(max_length = 250, choices = TYPES)
	url = models.CharField(max_length = 250)
	mark4 = models.IntegerField()
	mark6 = models.IntegerField()
	mark7 = models.IntegerField()
	mark8 = models.IntegerField()
	mark9 = models.IntegerField()
	mark10 = models.IntegerField()
	mark11 = models.IntegerField()
	
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
	student = models.ForeignKey('Student', blank = False, null = False)
	course = models.ForeignKey('Course', blank = False, null = False)
	mark = models.CharField(max_length = 250, choices = MARKS)

