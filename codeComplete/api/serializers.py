from rest_framework import serializers
from .models import Course, DashBoard, Submission, Assignment, Student, User

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'source', 'assignment', 'student', 'graded', 'points', 'pointsPossible', 'notes', 'onDashboard')

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('id','description', 'pointsPossible', 'name', 'course')
class CreateAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('description', 'pointsPossible', 'name', 'course')

class CreateSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('source', 'assignment', 'student')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'courses')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'courseName', 'teacher', 'code')

class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('courseName', 'teacher')

class DashSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashBoard
        fields = ('assignment', 'submissions')

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields =('id','graded','notes','points')

class GetAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('id','description','pointsPossible','name','course','graded')

class UserSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')