from django.db import models
from django.db.models.fields import Field
from django.db.models.fields.related import ManyToManyField
import random
import string

# Create your models here.

def generateCourseCode():
    length = 8
    isUnique = False

    while not isUnique:
        code = ''.join(random.choices(string.ascii_uppercase, k = length))
        print(code)
        if Course.objects.filter(code = code).count() == 0:
            isUnique= True

    return code


class Teacher(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

class Course(models.Model):
    courseName = models.CharField(max_length=50, blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    code = models.CharField(max_length=8, default=generateCourseCode, unique= True)

class Student(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    courses = models.ManyToManyField(Course)

class User(models.Model):
    username = models.CharField(primary_key=True, max_length=30, blank=False, null=False)
    password = models.CharField(max_length= 50, blank = False, null = False)
    isTeacher = models.BooleanField(default = False)
    teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE, null = True, blank=True)
    student = models.ForeignKey(Student, on_delete = models.CASCADE, null = True, blank = True)


class Assignment(models.Model):
    pointsPossible = models.FloatField(default=0)
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

class Submission(models.Model):
    source = models.TextField()
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    notes = models.TextField(default="", blank=True)
    graded = models.BooleanField(default=False)
    points = models.FloatField(default=0)
    pointsPossible = models.FloatField(default=0)
    onDashboard = models.BooleanField(default=False)


class DashBoard(models.Model):
    assignment = models.OneToOneField(Assignment, primary_key=True, on_delete=models.CASCADE)    
    submissions = models.ManyToManyField(Submission)


