from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from rest_framework import generics, status 
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import  *
from .models import Course, DashBoard, Student, Submission, Assignment, Teacher
import requests
import json
import base64
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class SubmissionView(APIView):
    serializer_class = SubmissionSerializer
    
    # get all of the student submissions for a given assignment
    def get(self, request, format=None):
        submissionQuery =Submission.objects.filter(assignment = request.GET.get('assignment'))
       
        if submissionQuery:
            submissions = []
            for submission in submissionQuery:
                currentSubmission = self.serializer_class(submission).data
                currentStudent = Student.objects.get(id=currentSubmission['student'])
                currentSubmission['studentName'] = currentStudent.name
                submissions.append(currentSubmission)
                
            return Response(submissions, status = status.HTTP_200_OK)
        
        return Response({"Bad Request":"No submissions"}, status = status.HTTP_404_NOT_FOUND)

class AssignmentView(APIView):
    # queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data = request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            print(serializer.data)
            assignmentQuery = Assignment.objects.filter(id=request.data.get('id'))
            print(assignmentQuery)
            if assignmentQuery:
                assignment = assignmentQuery[0]
                assignment.pointsPossible = serializer.data.get('pointsPossible')
                assignment.name = serializer.data.get('name')
                assignment.description = serializer.data.get('description')
                assignment.save()
                return Response({"Assignment Updated":"success"}, status = status.HTTP_200_OK)
        return Response({"Bad Request":"Assignment Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, format=None):
        assignment = Assignment.objects.get(id=request.GET.get('id'))
        if assignment:
            return Response(self.serializer_class(assignment).data,  status=status.HTTP_200_OK)
        else:
            return Response({"Bad Request":"Assignment Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self,request, format=None):
        serializer = CreateAssignmentSerializer(data = request.data)

        if serializer.is_valid():
            pointsPossible = serializer.data.get('pointsPossible')
            description = serializer.data.get('description')
            course = Course.objects.get(id=serializer.data.get('course'))
            name = serializer.data.get('name')
            assignment = Assignment(pointsPossible=pointsPossible, description=description, course = course, name = name)
            assignment.save()
            return Response({"Assignment Created":"success"}, status = status.HTTP_201_CREATED)
        else:
            return Response({"Bad request":"Invalid Assignment"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        assignment = Assignment.objects.get(id=request.data.get('id'))
        if assignment:
            assignment.delete()
            return Response({"Assignment Deleted":"success"}, status = status.HTTP_200_OK)
    
        return Response({"Bad request":"Invalid Assignment"}, status = status.HTTP_404_NOT_FOUND)
        

class getAssignments(APIView):
    serialize_class = AssignmentSerializer

    def post(self, request, format=None):
        courseid = request.data['id']
        student = None
        if request.data.get('student'):
            student = Student.objects.get(id = request.data.get('student'))
        assignmentQuerySet = Assignment.objects.filter(course = courseid)

        if(assignmentQuerySet.exists()):
            assignments = []
            for assignment in assignmentQuerySet:
                # print(assignment['name'])
                currentAssignment = AssignmentSerializer(assignment).data
                if student:
                    submissionQuerySet = Submission.objects.filter(student = student, assignment = assignment)
                    if submissionQuerySet:
                        submission= SubmissionSerializer(submissionQuerySet[0]).data
                        print(type(submission))
                        if submission['graded']:
                            currentAssignment['graded'] = True
                            currentAssignment['points'] = submission['points']
                        else:
                            currentAssignment['graded'] = False
                            currentAssignment['points'] = 0
                    else:
                        currentAssignment['graded'] = False
                        currentAssignment['points'] = 0
                assignments.append(currentAssignment)

            return Response(assignments, status=status.HTTP_200_OK)
        else:
            return Response({'Bad Request': 'No Open Assignments for this course'}, status=status.HTTP_400_BAD_REQUEST)

class CreateSubmissionView(APIView):
    serializer_class = CreateSubmissionSerializer

    def post(self, request, format=None):
        student = Student.objects.get(id=request.data['student'])
        source = request.data['source']
        assignment = Assignment.objects.get(id= request.data['assignment'])
        query = Submission.objects.filter(student=request.data['student'], assignment=request.data['assignment'])

        if query.exists():
            submission = query[0]
            if source == "" and submission.source != "":
                return Response(SubmissionSerializer(submission).data, status=status.HTTP_200_OK)
            else:
                submission.source = source
                submission.save(update_fields=['source'])
                return Response(SubmissionSerializer(submission).data, status=status.HTTP_200_OK)
        else:
            submission= Submission(source=source, student=student, assignment=assignment, pointsPossible=assignment.pointsPossible)
            submission.save()
            return Response(SubmissionSerializer(submission).data, status=status.HTTP_200_OK)

class GradeSubmission(APIView):
    serializerClass = GradeSerializer

    def post(self, request, format=None):
        serializer = self.serializerClass( data = request.data)
        print(request.data)

        if serializer.is_valid():
            print(serializer.data)
            submission = Submission.objects.get(id=request.data.get('id'))
            submission.graded = True
            submission.notes = serializer.data.get('notes')
            submission.points = serializer.data.get('points')
            submission.save()
            return Response({"AssignmentGraded":"Success"}, status=status.HTTP_200_OK)
        return Response({"AssignmentGraded":"Failure"},status=status.HTTP_404_NOT_FOUND)

 
class GetCourses(APIView):
    serialize_class = StudentSerializer
    lookup_url_kwarg = 'id'
    lookup_teacher_url = 'teacherID'

    def get(self, request, format=None):
        id = request.GET.get(self.lookup_url_kwarg)
        teacherID = request.GET.get(self.lookup_teacher_url)

        if id != None:
            student = Student.objects.filter(id=id)
            if len(student) > 0:
                data = StudentSerializer(student[0]).data
                courseId = data['courses']
                courses=[]
                for course in courseId:
                    courseQuerySet = Course.objects.filter(id=course)
                    currentCourse = CourseSerializer(courseQuerySet[0]).data
                    currentTeacher = Teacher.objects.filter(id=currentCourse['teacher'])
                    currentCourse['teacher'] = currentTeacher[0].name
                    courses.append(currentCourse)
                    print(currentCourse)
                print(courses)
                return Response(courses, status=status.HTTP_200_OK)
        elif  teacherID != None:
            courseQuerySet = Course.objects.filter(teacher=teacherID)
            courses = []
            for course in courseQuerySet:
                currentCourse = CourseSerializer(course).data
                courses.append(currentCourse)
            print(courses)
            return Response(courses, status=status.HTTP_200_OK)

        return Response({'StudentNotFound':'Invalid Student id'}, status=status.HTTP_404_NOT_FOUND)


class CreateCourse(APIView):
    serializeClass = CreateCourseSerializer

    def get(self, request, format=None):
        courseCode = request.GET.get('id')
        studentid = request.GET.get('studentid')
        if courseCode and studentid:
           querySet = Course.objects.filter(code = courseCode)
           student = Student.objects.get(id = studentid)
           if querySet and student:
               course = querySet[0]
               student.courses.add(course)
               return Response({"success":"Course added"}, status= status.HTTP_200_OK)
        else:
            return Response({"Failure":"Not Found"}, status = status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):


        serializer = self.serializeClass(data=request.data)

        if serializer.is_valid():
            courseName = serializer.data.get('courseName')
            teacher = Teacher.objects.get(id=serializer.data.get('teacher'))
            course = Course(courseName=courseName, teacher=teacher)
            course.save()

            return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, format=None):
        course = Course.objects.get(id=request.data['id'])
        if course:
            course.delete()
            return Response({"deleted":"success"}, status=status.HTTP_200_OK)
        else:
            return Response({"BadRequest":"invalid Course"}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def runCode(request):
    print(request.GET)
    respJSON = { "stdout": "test" }
    
    url = "https://judge0-ce.p.rapidapi.com/submissions"

    querystring = {"base64_encoded":"true","fields":"*"}

    payload = "{\"language_id\": 71,\"source_code\": \"" + request.GET['source'] +"\",\"stdin\": \"" + request.GET['input'] +"\"}"

    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "judge0-ce.p.rapidapi.com",
        'x-rapidapi-key': "9df88b19e0mshce2e66d4305a6a3p131542jsncd8f2046d7cd"
        }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    respJSON = json.loads(response.text)
    url = "https://judge0-ce.p.rapidapi.com/submissions/" + respJSON['token']

    querystring = {"base64_encoded":"true","fields":"*"}

    headers = {
        'x-rapidapi-host': "judge0-ce.p.rapidapi.com",
        'x-rapidapi-key': "9df88b19e0mshce2e66d4305a6a3p131542jsncd8f2046d7cd"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    respJSON = json.loads(response.text)
    print(respJSON['stderr'])
    return JsonResponse(respJSON['stdout'], safe=False)


class ExecuteSubmission(APIView):
    def post(self, request, format=None):
        serializer = SubmissionSerializer(data = request.data.get('submission'))
        input = request.data.get('input')
        print(input)
        print(request.data)
        print(serializer.is_valid())
        if serializer.is_valid():

            # byteLikeSource = serializer.data.get('source').encode('ascii')
            # byteLikeInput = input.encode('ascii')

            requestUrl = "https://judge0-ce.p.rapidapi.com/submissions"
            querystring = {"base64_encoded":"false","fields":"*"}
            headers = {
                'content-type': "application/json",
                'x-rapidapi-host': "judge0-ce.p.rapidapi.com",
                'x-rapidapi-key': "9df88b19e0mshce2e66d4305a6a3p131542jsncd8f2046d7cd"
            }
            payload = {
                'language_id': 71,
                'source_code': serializer.data.get('source'),
                'stdin': input,
            }

            payloadString = json.dumps(payload)
            print(payloadString)
            response = requests.request("POST",requestUrl,data = payloadString, headers=headers, params=querystring)
            JSONresponse = json.loads(response.text)

            requestUrl = "https://judge0-ce.p.rapidapi.com/submissions/{token}".format(token=JSONresponse['token'])
            querystring = {"base64_encoded":"false","fields":"*"}
            headers = {
                'x-rapidapi-host': "judge0-ce.p.rapidapi.com",
                'x-rapidapi-key': "9df88b19e0mshce2e66d4305a6a3p131542jsncd8f2046d7cd"
            }
            response = requests.request("GET", requestUrl, headers=headers, params=querystring)
            JSONresponse = json.loads(response.text)
            return Response(JSONresponse, status = status.HTTP_200_OK)



        return Response(status=status.HTTP_200_OK)


class Validate(APIView):
    def post(self, request, format=None):
        user = None
        userQuery = User.objects.filter(username = request.data.get('username'))
        if (userQuery):
            user = userQuery[0]
        if user:
            if user.password == request.data.get('password'):
                if user.isTeacher:
                    return Response({"Success":"teacher","teacher":user.teacher.id}, status = status.HTTP_200_OK)
                else:
                    return Response({"Success":"Student","student":user.student.id}, status = status.HTTP_200_OK)
        return Response({"failure":"invalid"}, status = status.HTTP_404_NOT_FOUND)

class Dash(APIView):



    # Need a function that will take an assignment number, and a submission
    # Then add the submission to the submission list
    # if the dashboard does not exist it should be created upon
    # a push to the dashboard
    def put(self,request, format=None):
        assignment = Assignment.objects.get(id = request.data.get('id'))
        submission = Submission.objects.get(id = request.data.get('submissionid'))
        submission.onDashboard = True
        submission.save()
        if not hasattr(assignment, 'dashboard'):
            dashboard = DashBoard(assignment = assignment)
            dashboard.save()
            dashboard.submissions.add(submission)
            
            print(dashboard)
        else:
            assignment.dashboard.submissions.add(submission)


        return Response({"Error":"OK"}, status = status.HTTP_200_OK)

    def get(self, request, format = None):
        print(request.GET.get('id'))
        dashboard = DashBoard.objects.get(assignment = request.GET.get('id'))
        if dashboard:
            dashData = DashSerializer(dashboard).data
            submissions = dashData.get('submissions')
            respSubmissions = []
            for submission in submissions:
                currentSubmission = Submission.objects.get(id = submission)
                serializedSubmission = SubmissionSerializer(currentSubmission).data
                serializedSubmission['studentName'] = currentSubmission.student.name
                respSubmissions.append(serializedSubmission)
            return Response(respSubmissions, status = status.HTTP_200_OK)
        return Response({"error":"dashboard Not Found"}, status = status.HTTP_200_OK)
    
    # A function that takes an assignment id, and returns all of the
    # submissions within the dashboard

    
    

    