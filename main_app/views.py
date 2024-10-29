from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from .models import Login
from .forms import LoginEntryForm, SignUpForm
import uuid, logging, json
from datetime import datetime

# Set up the logger
logger = logging.getLogger(__name__)

class Home(LoginView):
    
    # Home view to handle user login, extending Django's built-in LoginView.
    
    template_name = "home.html"

class CrudView(LoginRequiredMixin, View):
    
    # Handles Create, Read, Update, and Delete (CRUD) operations for password entries.
    
    model = Login
    form_class = LoginEntryForm
    template_name = "passwords/index.html"
    success_url = "/passwords"

    def get(self, request, *args, **kwargs):

        #Print GET password-id to see what's being passed in the request
        print("request.GET password-id: ", request.GET.get('password-id'))
        password_id = request.GET.get('password-id')
        # form = self.form_class()

        password = None  # Initialize password as None
        form = LoginEntryForm
        passwords = Login.objects.filter(user=request.user).order_by("appname")
        

        # If an ID is provided, load the specific password entry for updating
        if password_id:
            password = get_object_or_404(self.model, id=password_id, user=request.user)
            form = self.form_class(instance=password)
        else:
            form = self.form_class()

        
        # Pagination for listing passwords
        paginator = Paginator(passwords, 20)  # Show 20 passwords per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, 
                      { "passwords": passwords, "form": form, "password_id": password_id, "page_obj": page_obj, "password": password, })


    def post(self, request, *args, **kwargs):
        
        # Log request.POST data to see exactly what's passed in the request
        print("json dump POST: ", json.dumps(request.POST.dict()))
        # logger.info("POST data received: %s", json.dumps(request.POST.dict()))

        # Check for AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Log and return POST data as JSON for client-side logging
            return JsonResponse({'post_data': request.POST.dict()})

        # Handles create and update functionality.
        # Differentiates between 'save' and 'delete' actions based on the 'action' in POST data.

        print("Action is: ", request.POST.get('action'))
        action = request.POST.get('action')

        #Print POST password-id to see what's being passed in the request
        print("request.POST password-id: ", request.POST.get('password-id'))
        password_id = request.POST.get('password-id')

        if action == "delete" and password_id:
            print("Action does equal delete, issue must be in the return")
            return self.delete(request, password_id=password_id, *args, **kwargs)
        
        # Handle create or update
        if password_id:
            login_instance = get_object_or_404(self.model, id=password_id, user=request.user)
            form = self.form_class(request.POST, instance=login_instance)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            login_instance = form.save(commit=False)
            login_instance.user = request.user
            login_instance.save()
            print("login_instance: ", login_instance)
            print("login_instance.id: ", login_instance.id)
            print(request, "Password saved successfully.")
            messages.success(request, "Password saved successfully.")
            return redirect(self.success_url)
        
        # Pagination and form error handling
        passwords = Login.objects.filter(user=request.user).order_by("appname")
        paginator = Paginator(passwords, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        

        return render(request, self.template_name, {
            "page_obj": page_obj,
            "form": form,
            "password_id": password_id,
        })

    def delete(self, request, *args, password_id=None, **kwargs):
        
        # Handles deletion of a password entry.
        
        # password_id = kwargs.get("id")
        password_instance = get_object_or_404(self.model, id=password_id, user=request.user)
        password_instance.delete()
        messages.success(request, "Password deleted successfully.")
        return redirect(self.success_url)
    

@login_required
def password_detail(request, password_id):
    
    # Displays details for a single password entry.
    #use get_object_or_404 to handle non-existent objects gracefully and avoid a DoesNotExist exception
    #and check ownership of the password
    password = get_object_or_404(Login, id=password_id, user=request.user)
    return render(request, "passwords/detail.html", {"password": password})

def signup(request):
    
    # Handles user signup, including generating a UUID-based unique form ID and logging each signup attempt.
    
    form_id = f'signup-{uuid.uuid4()}'
    form = SignUpForm(request.POST or None, form_id=form_id)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful! Welcome!")
            logger.info(f"{timestamp} - Signup successful for username: {form.cleaned_data['username']}, email: {form.cleaned_data['email']}")
            return redirect("password-list")
        else:
            logger.error(f"{timestamp} - Signup failed. Errors: {form.errors.as_json()}")
            messages.error(request, "Invalid signup - please try again.")

    return render(request, "signup.html", {"form": form})

def ajax_login_view(request):
    
    # Handles AJAX-based login, returning JSON responses for success or failure.
    
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
    
    # API endpoint to check if the user is authenticated.
    
    return JsonResponse({
        'isAuthenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None
    })

@login_required
def simple_password_create(request):
    
    # Simplified view for creating a new password entry.
    
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


# def check_authentication_status(request):
#     # API endpoint to check if the user is authenticated
#     return JsonResponse({
#         'isAuthenticated': request.user.is_authenticated,
#         'username': request.user.username if request.user.is_authenticated else None
#     })


# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import JsonResponse
# from django.views.generic.edit import CreateView, UpdateView
# from django.views import View
# from django.contrib import messages
# from django.contrib.auth import authenticate, login
# from django.http import JsonResponse
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.views import LoginView
# from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.paginator import Paginator

# from .models import Login
# from .forms import LoginEntryForm, SignUpForm

# import logging
# from datetime import datetime

# import uuid
# from datetime import datetime


# class Home(LoginView):
#     template_name = "home.html"

# class PassCreate(CreateView):
#     model = Login
#     fields = ["username", "password", "note"]

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
    
# # Create an API endpoint to check if the user is authenticated
# def check_authentication_status(request):
#     return JsonResponse({'isAuthenticated': request.user.is_authenticated, 'username': request.user.username if request.user.is_authenticated else None})

# @login_required
# def password_index(request):
#     passwords = Login.objects.filter(user=request.user).select_related('user')
    
#     # Implement pagination with 10 items per page
#     paginator = Paginator(passwords, 20)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, "passwords/index.html", {"page_obj": page_obj})


# @login_required
# def password_detail(request, password_id):
#     #use get_object_or_404 to handle non-existent objects gracefully and avoid a DoesNotExist exception
#     #and check ownership of the password
#     password = get_object_or_404(Login, id=password_id, user=request.user)
#     return render(request, "passwords/detail.html", {"password": password})

# import logging
# from datetime import datetime

# # Set up the logger
# logger = logging.getLogger(__name__)

# # for updating the error messages in the login form in the showcase menu
# def ajax_login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             # If login is successful, log the user in and return success
#             user = form.get_user()
#             login(request, user)
#             return JsonResponse({'success': True, 'username': user.username})
#         else:
#             # Collect errors to send them back to the client
#             errors = [error for error_list in form.errors.values() for error in error_list]
#             return JsonResponse({'success': False, 'errors': errors})
#     return JsonResponse({'success': False, 'errors': ['Invalid request']})

# def signup(request):
#     # Generate a UUID-based unique form_id
#     form_id = f'signup-{uuid.uuid4()}'
#     print(f"Form ID: {form_id}")  # Add this line for debugging
#     form = SignUpForm(request.POST or None, form_id=form_id)
    
#     # Capture the current timestamp for logging
#     timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     if request.method == "POST":
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Signup successful! Welcome!")
#             logger.info(f"{timestamp} - Signup successful for username: {form.cleaned_data['username']}, email: {form.cleaned_data['email']}")
#             return redirect("password-index")
#         else:
#             logger.error(f"{timestamp} - Signup failed. Errors: {form.errors.as_json()}")
#             messages.error(request, "Invalid Signup - Try again")

#     return render(request, "signup.html", {"form": form})

# class PassCreate(LoginRequiredMixin, CreateView):
#     model = Login
#     fields = ["username", "password", "note"]

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


# class PassUpdate(LoginRequiredMixin, UpdateView):
#     model = Login
#     fields = ["username", "password", "note"]
#     template_name = 'passwords/update.html'

#     def get_queryset(self):
#         return Login.objects.filter(user=self.request.user)

#     def post(self, request, *args, **kwargs):
#         action = request.POST.get('action')
#         if action == 'delete':
#             return self.delete(request, *args, **kwargs)
#         return super().post(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         password_id = kwargs.get('pk')  # Get the password ID from the URL
#         password_instance = get_object_or_404(self.model, id=password_id, user=request.user)
#         password_instance.delete()
#         messages.success(request, "Password deleted successfully.")
#         return redirect("password-index")  # Redirect after deletion

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         messages.success(request, "Password updated successfully.")
#         return super().form_valid(form)



# class CrudView(LoginRequiredMixin, View):
#     model = Login
#     form_class = LoginEntryForm
#     template_name = "passwords/index.html"
#     success_url = "/passwords"

#     def get(self, request, *args, **kwargs):
#         password_id = kwargs.get("id")

#         form = LoginEntryForm
#         passwords = Login.objects.filter(user=request.user).order_by("appname")


#         if password_id:
#             login_instance = get_object_or_404(self.model, id=password_id)
#             form = self.form_class(instance=login_instance)
#         else:
#             form = self.form_class()
#         return render(
#             request,
#             "passwords/index.html",
#             {"passwords": passwords, "form": form, "password_id": password_id},
#         )





#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             login_instance = form.save(commit=False)
#             login_instance.user = request.user
#             login_instance.save()
#             return redirect(self.success_url)
#         else:
#             print(form.errors)
#             passwords = Login.objects.filter(user=request.user).order_by("appname")
#             return render(
#                 request, self.template_name, {"passwords": passwords, "form": form}
#             )

#     def put(self, request, *args, **kwargs):
#         login_id = kwargs.get("id")
#         login = get_object_or_404(Login, id=login_id)

#         form = LoginEntryForm(request.PUT, instance=login)

#         passwords = Login.objects.filter(user=request.user).order_by("appname")
#         return render(
#             request, self.template_name, {"form": form, "passwords": passwords}
#         )












# def simple_password_create(request):
#     if request.method == "POST":
#         form = LoginEntryForm(request.POST)
#         if form.is_valid():
#             login_instance = form.save(commit=False)
#             login_instance.user = request.user
#             login_instance.save()
#             return redirect("/passwords/")
#     else:
#         form = LoginEntryForm()
#     return render(request, "passwords/index.html", {"form": form})
