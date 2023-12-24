from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    course_id_1 = models.IntegerField(default=0)
    course_id_2 = models.IntegerField(default=0)
    course_id_3 = models.IntegerField(default=0)

    def __str__(self):
        return (f"{self.middle_name} {self.first_name} {self.last_name}")


class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    name_of_teacher = models.CharField(max_length=100)
    number_of_students = models.IntegerField(default=0)

    def __str__(self):
        return (f"{self.title} ({self.name_of_teacher})")
