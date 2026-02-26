from django.db import models
from django.contrib.auth.models import User
from principal.models import Department
from datetime import date
from cloudinary.models import CloudinaryField

class Student(models.Model):
    role = models.CharField(max_length=50, null=False, default='student')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    reg_number = models.CharField(max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    year_of_admission = models.IntegerField(default=date.today().year)
    phone_number = models.CharField(max_length=10, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True)
    profil = CloudinaryField('image', null=True, blank=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username