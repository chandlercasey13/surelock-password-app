
from django.shortcuts import render
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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
    
@login_required
def password_index(request):
    passwords = Login.objects.filter(user=request.user)
   
    return render(request, 'passwords/index.html', {'passwords': passwords})


def password_detail(request, password_id):
    password = Login.objects.get(id=password_id)
    return render(request, 'passwords/detail.html', {'password': password})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )

