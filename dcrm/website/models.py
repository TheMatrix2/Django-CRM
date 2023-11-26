from django.db import models


class Client(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.CharField(max_length=100, auto_created=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return (f"{self.first_name} {self.middle_name} {self.last_name}")
