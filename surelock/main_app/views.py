
from django.shortcuts import render
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from .models import Login #imports Login model from models.py
 
class Home(LoginView):
    template_name = 'home.html'

class PassCreate(CreateView):
    model = Login
    fields = ['username', 'password', 'note']

    # This inherited method is called when a
    # valid login/password form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)

def password_index(request):
    # Render the passwords/index.html template with the cats data
    passwords = Login.objects.all()
    return render(request, 'passwords/index.html', {'passwords': passwords})


def password_detail(request, password_id):
    password = Login.objects.get(id=password_id)
    return render(request, 'passwords/detail.html', {'password': password})


