import uuid
import logging
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from datetime import datetime
from .forms import LoginEntryForm, SignUpForm
from .models import Login, Profile

# Initialize the logger for structured logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Home(LoginView):
    # User login view, extending Django's built-in LoginView
    template_name = "home.html"

class CrudView(LoginRequiredMixin, View):
    # View to handle Create, Read, Update, and Delete (CRUD) operations for password entries
    # Requires login, so it inherits LoginRequiredMixin

    model = Login
    form_class = LoginEntryForm
    template_name = "passwords/list.html"
    success_url = reverse_lazy('password-list')

    def get(self, request, *args, **kwargs):
        logger.info("GET request received for password list view.")
        # Activate the user's timezone
        user_timezone = request.user.profile.timezone
        timezone.activate(user_timezone)

        # Retrieve password ID for update if provided
        password_id = request.GET.get('password-id')
        password = None

        # Set up form instance; prefill if updating an existing password entry
        form = self.form_class()
        if password_id:
            password = get_object_or_404(self.model, id=password_id, user=request.user)
            form = self.form_class(instance=password)
            logger.info(f"Editing existing password entry: ID = {password_id}")
        # Fetch and paginate all user passwords
        passwords = Login.objects.filter(user=request.user).order_by("appname")
        logger.info(f"Number of password entries retrieved: {passwords.count()}")

        page_obj = Paginator(passwords, 20).get_page(request.GET.get('page'))

        # Render the password list page with form and pagination context
        response = render(request, self.template_name, {
            "passwords": passwords,
            "form": form,
            "password_id": password_id,
            "page_obj": page_obj,
            "password": password,
        })

        timezone.deactivate()  # Reset timezone after rendering
        return response

    def post(self, request, *args, **kwargs):
        logger.info("POST request received for password entry creation/update.")

        action = request.POST.get('action')
        # logger.info(f"Action from form: {action}")
        # if action not in ["save", "delete"]:
        #     messages.error(request, "Invalid action.")
        #     logger.info("Invalid action: ")
        #     return redirect(self.success_url)
        
        password_id = request.POST.get('password-id')
        logger.info("Password ID from form: {password_id}")
        # Handle deletion
        if action == "delete" and password_id:
            return self.delete(request, password_id=password_id, *args, **kwargs)
        
        # Handle create or update
        login_instance = get_object_or_404(self.model, id=password_id, user=request.user) if password_id else None
        form = self.form_class(request.POST, instance=login_instance)
        logger.info("Form instance created.", form)
        logger.info("login_instance: ", login_instance)

        if form.is_valid():
            logger.info("Form is valid.")
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, "Password saved successfully.")
            logger.info(f"Password entry saved: ID = {entry.id}, App Name = {entry.appname}")
             # Log the database queries executed (to confirm database interaction)
            for query in connection.queries:
                logger.debug(query)

            return redirect(self.success_url)    
        else:
            logger.info("Form is invalid.")
            logger.error(f"Form is invalid: {form.errors}")
        
        passwords = Login.objects.filter(user=request.user).order_by("appname")
        page_obj = Paginator(passwords, 20).get_page(request.GET.get('page'))

        return render(request, self.template_name, {
            "page_obj": page_obj,
            "form": form,
            "password_id": password_id,
        })
         
    def delete(self, request, *args, password_id=None, **kwargs):
        password_instance = get_object_or_404(self.model, id=password_id, user=request.user)
        password_instance.delete()
        messages.success(request, "Password deleted successfully.")
        return redirect(self.success_url)

@login_required
def password_detail(request, password_id):
    user_timezone = request.user.profile.timezone
    timezone.activate(user_timezone)

    password = get_object_or_404(Login, id=password_id, user=request.user)
    response = render(request, "passwords/detail.html", {"password": password})

    timezone.deactivate()
    return response

def signup(request):
    form_id = f'signup-{uuid.uuid4()}'
    form = SignUpForm(request.POST or None, form_id=form_id)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            # Ensure profile is created and save timezone
            profile, created = Profile.objects.get_or_create(user=user)
            profile.timezone = form.cleaned_data.get('timezone')
            profile.save()
            login(request, user)
            messages.success(request, "Signup successful! Welcome!")
            logger.info(f"{timestamp} - Signup successful for username: {form.cleaned_data['username']}")
            return redirect("password-list")
        else:
            logger.error(f"{timestamp} - Signup failed. Errors: {form.errors.as_json()}")
            messages.error(request, "Invalid signup - please try again.")
           

    return render(request, "signup.html", {"form": form})

def ajax_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({'success': True, 'username': user.username})
        else:
            errors = [error for error_list in form.errors.values() for error in error_list]
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'errors': ['Invalid request']})

def check_authentication_status(request):
    return JsonResponse({
        'isAuthenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None
    })

@login_required
def simple_password_create(request):
    if request.method == "POST":
        form = LoginEntryForm(request.POST)
        if form.is_valid():
            login_instance = form.save(commit=False)
            login_instance.user = request.user
            login_instance.save()
            messages.success(request, "Password created successfully.")
            return redirect("password-list")
    else:
        form = LoginEntryForm()
    return render(request, "passwords/simple_create.html", {"form": form})

@login_required
def bulk_delete_view(request):
    if request.method == "POST":
        selected_passwords = request.POST.getlist("selected_passwords")
        if selected_passwords:
            Login.objects.filter(id__in=selected_passwords, user=request.user).delete()
            messages.success(request, f"{len(selected_passwords)} password(s) deleted successfully.")
        else:
            messages.warning(request, "No passwords selected for deletion.")
    return redirect("password-list")
