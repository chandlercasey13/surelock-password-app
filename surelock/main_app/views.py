
from django.shortcuts import render

from .models import Password
 
def home(request):
    return render(request, 'index.html')


def password_index(request):
    # Render the cats/index.html template with the cats data
    passwords = Password.objects.all()
    return render(request, 'passwords/index.html', {'passwords': passwords})


def password_detail(request, password_id):
    password = Password.objects.get(id=password_id)
    return render(request, 'passwords/detail.html', {'password': password})




