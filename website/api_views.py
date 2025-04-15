from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Client, Course
from .serializers import (
    UserSerializer, ClientSerializer, CourseSerializer, CourseDetailSerializer
)


# Authentication endpoints
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        login(request, user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'message': 'Вы вошли в систему!'
        })


@api_view(['POST'])
def logout_view(request):
    # Clear the auth token
    if request.user.is_authenticated:
        Token.objects.filter(user=request.user).delete()
        logout(request)
    return Response({"message": "Вы вышли из системы"})


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                # Set password
                user.set_password(request.data.get('password'))
                user.save()

                # Login the user
                login(request, user)

                # Create token for API access
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': serializer.data,
                    'message': 'Успешная регистрация! Добро пожаловать!'
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


# Client viewset
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Get available clients for a course (not already enrolled and have space)
    @action(detail=False, methods=['get'])
    def available_for_course(self, request):
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response({"error": "course_id parameter is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Find clients not in this course and who have an available course slot
        clients = (Client.objects.exclude(course_id_1=course_id) &
                   Client.objects.exclude(course_id_2=course_id) &
                   Client.objects.exclude(course_id_3=course_id) &
                   (Client.objects.filter(course_id_1=0) |
                    Client.objects.filter(course_id_2=0) |
                    Client.objects.filter(course_id_3=0)))

        serializer = self.get_serializer(clients, many=True)
        return Response(serializer.data)


# Course viewset
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Update the number of students before sending the response
        students = (Client.objects.filter(course_id_1=instance.id) |
                    Client.objects.filter(course_id_2=instance.id) |
                    Client.objects.filter(course_id_3=instance.id))
        instance.number_of_students = students.count()
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Add students to a course
    @action(detail=True, methods=['post'])
    def add_students(self, request, pk=None):
        course = self.get_object()
        student_ids = request.data.get('student_ids', [])

        results = {
            'success': [],
            'errors': []
        }

        for student_id in student_ids:
            try:
                student = Client.objects.get(id=student_id)
                student_courses = [student.course_id_1, student.course_id_2, student.course_id_3]

                # Check if student is already enrolled
                if int(pk) in student_courses:
                    results['errors'].append({
                        'id': student.id,
                        'name': f"{student.first_name} {student.last_name}",
                        'message': 'Клиент уже числится на этом курсе'
                    })
                    continue

                # Check if student has available course slots
                if 0 in student_courses:
                    # Add to first available slot
                    index = student_courses.index(0)
                    student_courses[index] = int(pk)

                    # Update student
                    student.course_id_1 = student_courses[0]
                    student.course_id_2 = student_courses[1]
                    student.course_id_3 = student_courses[2]
                    student.save()

                    # Update course count
                    course.number_of_students += 1
                    course.save()

                    results['success'].append({
                        'id': student.id,
                        'name': f"{student.first_name} {student.last_name}",
                        'message': 'Клиент зачислен на курс'
                    })
                else:
                    results['errors'].append({
                        'id': student.id,
                        'name': f"{student.first_name} {student.last_name}",
                        'message': 'Клиент уже числится на максимально возможном количестве курсов (3)'
                    })
            except Client.DoesNotExist:
                results['errors'].append({
                    'id': student_id,
                    'message': f'Клиент с ID {student_id} не найден'
                })

        return Response(results)

    # Remove a student from a course
    @action(detail=True, methods=['post'])
    def remove_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')

        if not student_id:
            return Response({"error": "student_id is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Client.objects.get(id=student_id)
            student_courses = [student.course_id_1, student.course_id_2, student.course_id_3]

            if int(pk) in student_courses:
                # Remove course from student's list
                index = student_courses.index(int(pk))
                student_courses[index] = 0

                # Update student
                student.course_id_1 = student_courses[0]
                student.course_id_2 = student_courses[1]
                student.course_id_3 = student_courses[2]
                student.save()

                # Update course count
                course.number_of_students -= 1
                course.save()

                return Response({
                    "message": "Клиент больше не учится на этом курсе",
                    "student": {
                        "id": student.id,
                        "name": f"{student.first_name} {student.last_name}"
                    }
                })
            else:
                return Response({"error": "На этом курсе нет такого клиента"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Client.DoesNotExist:
            return Response({"error": f"Клиент с ID {student_id} не найден"},
                            status=status.HTTP_404_NOT_FOUND)


# Simple API endpoint to get current user status
@api_view(['GET'])
def check_auth(request):
    if request.user.is_authenticated:
        return Response({
            "authenticated": True,
            "user": UserSerializer(request.user).data
        })
    else:
        return Response({"authenticated": False})