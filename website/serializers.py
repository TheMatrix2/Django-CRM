from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Course


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class ClientSerializer(serializers.ModelSerializer):
    course_title_1 = serializers.SerializerMethodField(read_only=True)
    course_title_2 = serializers.SerializerMethodField(read_only=True)
    course_title_3 = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

    def get_course_title_1(self, obj):
        if obj.course_id_1 != 0:
            try:
                course = Course.objects.get(id=obj.course_id_1)
                return course.title
            except Course.DoesNotExist:
                return None
        return None

    def get_course_title_2(self, obj):
        if obj.course_id_2 != 0:
            try:
                course = Course.objects.get(id=obj.course_id_2)
                return course.title
            except Course.DoesNotExist:
                return None
        return None

    def get_course_title_3(self, obj):
        if obj.course_id_3 != 0:
            try:
                course = Course.objects.get(id=obj.course_id_3)
                return course.title
            except Course.DoesNotExist:
                return None
        return None


class CourseSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_students_count(self, obj):
        return (Client.objects.filter(course_id_1=obj.id) |
                Client.objects.filter(course_id_2=obj.id) |
                Client.objects.filter(course_id_3=obj.id)).count()


class CourseDetailSerializer(CourseSerializer):
    students = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_students(self, obj):
        students = (Client.objects.filter(course_id_1=obj.id) |
                    Client.objects.filter(course_id_2=obj.id) |
                    Client.objects.filter(course_id_3=obj.id))
        return ClientSerializer(students, many=True).data