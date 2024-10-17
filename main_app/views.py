from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import Login
from .forms import LoginEntryForm, SignUpForm

import logging
from datetime import datetime

import uuid
from datetime import datetime


class Home(LoginView):
    template_name = "home.html"

class PassCreate(CreateView):
    model = Login
    fields = ["username", "password", "note"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def password_index(request):
    passwords = Login.objects.filter(user=request.user).select_related('user')
    
    # Implement pagination with 10 items per page
    paginator = Paginator(passwords, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "passwords/index.html", {"page_obj": page_obj})


@login_required
def password_detail(request, password_id):
    #use get_object_or_404 to handle non-existent objects gracefully and avoid a DoesNotExist exception
    #and check ownership of the password
    password = get_object_or_404(Login, id=password_id, user=request.user)
    return render(request, "passwords/detail.html", {"password": password})

import logging
from datetime import datetime

# Set up the logger
logger = logging.getLogger(__name__)

def signup(request):
    # Generate a UUID-based unique form_id
    form_id = f'signup-{uuid.uuid4()}'
    print(f"Form ID: {form_id}")  # Add this line for debugging
    form = SignUpForm(request.POST or None, form_id=form_id)
    
    # Capture the current timestamp for logging
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful! Welcome!")
            logger.info(f"{timestamp} - Signup successful for username: {form.cleaned_data['username']}, email: {form.cleaned_data['email']}")
            return redirect("password-index")
        else:
            logger.error(f"{timestamp} - Signup failed. Errors: {form.errors.as_json()}")
            messages.error(request, "Invalid Signup - Try again")

    return render(request, "signup.html", {"form": form})

class PassCreate(LoginRequiredMixin, CreateView):
    model = Login
    fields = ["username", "password", "note"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PassUpdate(LoginRequiredMixin, UpdateView):
    model = Login
    fields = ["username", "password", "note"]
    template_name = 'passwords/update.html'

    def get_queryset(self):
        return Login.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CrudView(LoginRequiredMixin, View):
    model = Login
    form_class = LoginEntryForm
    template_name = "passwords/index.html"
    success_url = "/passwords"

    def get(self, request, *args, **kwargs):
        password_id = kwargs.get("id")

        form = LoginEntryForm
        passwords = Login.objects.filter(user=request.user).order_by("appname")


        if password_id:
            login_instance = get_object_or_404(self.model, id=password_id)
            form = self.form_class(instance=login_instance)
        else:
            form = self.form_class()
        return render(
            request,
            "passwords/index.html",
            {"passwords": passwords, "form": form, "password_id": password_id},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            login_instance = form.save(commit=False)
            login_instance.user = request.user
            login_instance.save()
            return redirect(self.success_url)
        else:
            print(form.errors)
            passwords = Login.objects.filter(user=request.user).order_by("appname")
            return render(
                request, self.template_name, {"passwords": passwords, "form": form}
            )

    def put(self, request, *args, **kwargs):
        login_id = kwargs.get("id")
        login = get_object_or_404(Login, id=login_id)

        form = LoginEntryForm(request.PUT, instance=login)

        passwords = Login.objects.filter(user=request.user).order_by("appname")
        return render(
            request, self.template_name, {"form": form, "passwords": passwords}
        )

def delete(self, request, *args, **kwargs):
    password_id = kwargs.get("id")
    password_instance = get_object_or_404(self.model, id=password_id, user=request.user)
    password_instance.delete()
    return redirect("password-index")



def simple_password_create(request):
    if request.method == "POST":
        form = LoginEntryForm(request.POST)
        if form.is_valid():
            login_instance = form.save(commit=False)
            login_instance.user = request.user
            login_instance.save()
            return redirect("/passwords/")
    else:
        form = LoginEntryForm()
    return render(request, "passwords/index.html", {"form": form})
