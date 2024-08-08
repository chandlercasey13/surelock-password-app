from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from django.views.generic.edit import CreateView, UpdateView

from django.views import View

from .models import Login
from .forms import LoginForm
from .forms import SignUpForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Login


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
    passwords = Login.objects.filter(user=request.user)

    return render(request, "passwords/index.html", {"passwords": passwords})


@login_required
def password_detail(request, password_id):
    password = Login.objects.get(id=password_id)
    return render(request, "passwords/detail.html", {"password": password})

#ORIGINAL CODE BEFORE MY ATTEMPT AT A CUSTOM SIGNUP
# def signup(request):
#     error_message = ""
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("password-index")
#         else:
#             error_message = "Invalid Signup - Try again"
#     form = UserCreationForm()
#     context = {"form": form, "error_message": error_message}
#     return render(request, "signup.html", context)

#THIS IS THE NEW CODE
def signup(request):
    error_message = ""
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("password-index")
        else:
            error_message = "Invalid Signup - Try again"
    form = SignUpForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "signup.html", context)

class PassCreate(LoginRequiredMixin, CreateView):
    model = Login
    form_class = LoginForm
    template_name = "passwords/index.html"
    success_url = "/passwords"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["passwords"] = Login.objects.all()
        return context


class PasswordUpdate(LoginRequiredMixin, UpdateView):
    model = Login
    form_class = LoginForm
    template_name = "passwords/index.html"
    success_url = "/passwords/"

    def get(self, request, *args, **kwargs):
        password_id = kwargs.get("pk")

        form = LoginForm
        passwords = Login.objects.filter(user=request.user).order_by("id")

        if password_id:
            login_instance = get_object_or_404(self.model, id=password_id)
            form = self.form_class(instance=login_instance)
        else:
            form = self.form_class()
        return render(
            request,
            "passwords/index.html",
            {"passwords": passwords, "updateform": form, "password_id": password_id},
        )


class CrudView(LoginRequiredMixin, View):
    model = Login
    form_class = LoginForm
    template_name = "passwords/index.html"
    success_url = "/passwords"

    def get(self, request, *args, **kwargs):
        password_id = kwargs.get("id")

        form = LoginForm
        passwords = Login.objects.filter(user=request.user).order_by("id")

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
            passwords = Login.objects.filter(user=request.user)
            return render(
                request, self.template_name, {"passwords": passwords, "form": form}
            )

    def put(self, request, *args, **kwargs):
        login_id = kwargs.get("id")
        login = get_object_or_404(Login, id=login_id)

        form = LoginForm(request.PUT, instance=login)

        passwords = Login.objects.all()
        return render(
            request, self.template_name, {"form": form, "passwords": passwords}
        )

    def delete(self, request, *args, **kwargs):
        password_id = kwargs.get("id")
        password_instance = get_object_or_404(self.model, id=password_id)
        password_instance.delete()
        return JsonResponse({"message": "Password deleted successfully!"}, status=200)


def simple_password_create(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login_instance = form.save(commit=False)
            login_instance.user = request.user
            login_instance.save()
            return redirect("/passwords/")
    else:
        form = LoginForm()
    return render(request, "passwords/index.html", {"form": form})
