from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        """Department object name displayed in admin panel"""
        return self.name



class User(AbstractUser):
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    family_name = models.CharField(max_length=100, null=True)
    count_trainings = models.IntegerField(default=0, null=True)

    @property
    def registered_2_courses(self):
        """"Returning whether a user registered 2 courses or less, if 2 so he won't be able to register more than 2"""
        if self.count_trainings == 2:
            return False
        else:
            return True

    def __str__(self):
        """User object name displayed in admin panel"""
        return f"{self.id}: {self.username}"