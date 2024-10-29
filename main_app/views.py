from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Login
from .forms import LoginEntryForm, SignUpForm
import uuid
import logging
from datetime import datetime

# Initialize the logger for structured logging
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
    success_url = reverse_lazy('password-list')  # Using reverse_lazy for flexibility

    def get(self, request, *args, **kwargs):
        # Displays all password entries and the form for creating or updating entries
        # Retrieves password_id from GET params for updating, if available
        
        # Retrieve password ID for update if provided
        password_id = request.GET.get('password-id')
        password = None  # Initialize password to None

        # Set up form instance; prefill if updating an existing password entry
        form = self.form_class()
        if password_id:
            password = get_object_or_404(self.model, id=password_id, user=request.user)
            form = self.form_class(instance=password)

        # Fetch and paginate all user passwords
        passwords = Login.objects.filter(user=request.user).order_by("appname")
        page_obj = Paginator(passwords, 20).get_page(request.GET.get('page'))

        # Render the password list page with form and pagination context
        return render(request, self.template_name, {
            "passwords": passwords,
            "form": form,
            "password_id": password_id,
            "page_obj": page_obj,
            "password": password,
        })

    def post(self, request, *args, **kwargs):
        # Handles form submissions for creating, updating, or deleting password entries
        # Differentiates actions based on 'action' field in POST data ('save' or 'delete')
        
        # Determine the action (save or delete) and validate it
        action = request.POST.get('action')
        if action not in ["save", "delete"]:
            messages.error(request, "Invalid action.")
            return redirect(self.success_url)
        
        # Retrieve password ID for update or delete
        password_id = request.POST.get('password-id')
        
        # Handle deletion
        if action == "delete" and password_id:
            return self.delete(request, password_id=password_id, *args, **kwargs)
        
        # Handle create or update
        login_instance = get_object_or_404(self.model, id=password_id, user=request.user) if password_id else None
        form = self.form_class(request.POST, instance=login_instance)

        # Validate and save form data
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, "Password saved successfully.")
            return redirect(self.success_url)
        
        # If form is invalid, re-render the form with errors and paginated password entries
        passwords = Login.objects.filter(user=request.user).order_by("appname")
        page_obj = Paginator(passwords, 20).get_page(request.GET.get('page'))

        return render(request, self.template_name, {
            "page_obj": page_obj,
            "form": form,
            "password_id": password_id,
        })

    def delete(self, request, *args, password_id=None, **kwargs):
        # Handles the deletion of a password entry based on password_id
        # Checks user ownership before deletion
        
        # Fetch and delete the password instance
        password_instance = get_object_or_404(self.model, id=password_id, user=request.user)
        password_instance.delete()
        messages.success(request, "Password deleted successfully.")
        return redirect(self.success_url)
    

@login_required
def password_detail(request, password_id):
    # Displays details for a specific password entry
    # Uses get_object_or_404 to ensure the password exists and is owned by the user
    
    password = get_object_or_404(Login, id=password_id, user=request.user)
    return render(request, "passwords/detail.html", {"password": password})

def signup(request):
    # Handles user signup by creating a new account and logging in the user upon success
    # Uses a UUID-based form ID for tracking and logs each signup attempt
    
    form_id = f'signup-{uuid.uuid4()}'
    form = SignUpForm(request.POST or None, form_id=form_id)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful! Welcome!")
            logger.info(f"{timestamp} - Signup successful for username: {form.cleaned_data['username']}")
            return redirect("password-list")
        else:
            logger.error(f"{timestamp} - Signup failed. Errors: {form.errors.as_json()}")
            messages.error(request, "Invalid signup - please try again.")

    return render(request, "signup.html", {"form": form})

def ajax_login_view(request):
    # Handles AJAX-based login, returns JSON responses indicating success or failure
    # Responds with user data on successful login and error messages otherwise
    
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
    # API endpoint to check if the user is authenticated
    # Returns JSON response with authentication status and username if logged in
    
    return JsonResponse({
        'isAuthenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None
    })

@login_required
def simple_password_create(request):
    # Simplified view for creating a new password entry
    # Handles form validation and redirects to password list on success
    
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
