
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Login
from .forms import LoginForm
 
def home(request):
    return render(request, 'index.html')


def password_index(request):
    # Render the cats/index.html template with the cats data
    passwords = Login.objects.all()
    return render(request, 'passwords/index.html', {'passwords': passwords})


def password_detail(request, password_id):
    password = Login.objects.get(id=password_id)
    return render(request, 'passwords/detail.html', {'password': password})


class PassCreate(CreateView):
    model = Login
    form_class = LoginForm
    template_name = 'passwords/index.html'
    success_url = '/passwords'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['passwords'] = Login.objects.all()
        return context
    
