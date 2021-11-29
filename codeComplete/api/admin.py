from django.contrib import admin
from .models import DashBoard, Student, Submission, Assignment, Teacher, Course, User
# Register your models here.
admin.site.register(Submission)
admin.site.register(Assignment)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(User)
admin.site.register(DashBoard)