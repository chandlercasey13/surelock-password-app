
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views import View

from .models import Login
from .forms import LoginForm
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



class PassCreate(CreateView):
    model = Login
    form_class = LoginForm
    template_name = 'passwords/index.html'
    success_url = '/passwords'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['passwords'] = Login.objects.all()
        return context
    

class PasswordUpdate(UpdateView):
    model = Login
    fields = ["appname", "username", "password", "note"]

class PasswordDelete(DeleteView):
    model = Login
    success_url = "/passwords/"



class CrudView(View):
    model = Login
    form_class = LoginForm
    template_name = 'passwords/index.html'
    success_url = '/passwords'
    
    def get(self, request, *args, **kwargs):
        form = LoginForm
        passwords = Login.objects.all()
        return render(request,'passwords/index.html', {'passwords': passwords, 'form': form}  )
    

    def post(self,request, *args, **kwargs):
        form = LoginForm(request.POST)
        form.save()
        passwords = Login.objects.all()
        
        return render(request, self.template_name, {'passwords': passwords, 'form': form})
    
    # def put(self, request, *args, **kwargs):
    #     login_id = kwargs.get('id')
    #     login = get_object_or_404(Login, id=login_id)

    #     form = LoginForm(request.PUT, instance= login)

    #     passwords = Login.objects.all()
    #     return render(request, self.template_name, {'form': form, 'passwords': passwords})


    

    


