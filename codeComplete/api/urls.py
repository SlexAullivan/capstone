
from django.urls import path
from .views import *

urlpatterns = [ 
    path('submission', SubmissionView.as_view()),
    path('assignment', AssignmentView.as_view()),
    path('createSubmission', CreateSubmissionView.as_view()),
    path('get-courses', GetCourses.as_view()),
    path('create-course', CreateCourse.as_view()),
    path('runCode', runCode, name = "runCode"),
    path('get-assignments', getAssignments.as_view()),
    path('grade', GradeSubmission.as_view()),
    path('execute', ExecuteSubmission.as_view()),
    path('validate',Validate.as_view()),
    path('dashboard', Dash.as_view())
]