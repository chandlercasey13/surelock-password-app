from django.db import models

# Import the User
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Login(models.Model):
    appname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    note = models.TextField(max_length=250, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_datetime = models.DateTimeField()
    

    def __str__(self):
        return self.appname
