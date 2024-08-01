
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .models import Login #imports Login model from models.py
 
class Home(LoginView):
    template_name = 'home.html'

def password_index(request):
    # Render the passwords/index.html template with the cats data
    passwords = Login.objects.all()
    return render(request, 'passwords/index.html', {'passwords': passwords})


def password_detail(request, password_id):
    password = Login.objects.get(id=password_id)
    return render(request, 'passwords/detail.html', {'password': password})


