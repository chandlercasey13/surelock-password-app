from django.db import models

# Create your models here.

class Login(models.Model):
    appname = models.CharField(default='No App Name', max_length=100)
    username =  models.CharField(default = 'No Username', max_length=100)
    password =  models.CharField(default = 'No Password', max_length=100)
    note = models.TextField(default= 'Nothing Here', max_length=250)

    def __str__(self):
        return self.appname    
