# main_app/context_processors.py
from .forms import UserLoginForm

def login_form_processor(request):
    return {
        'login_form': UserLoginForm()
    }