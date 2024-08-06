from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views import View

from .models import Login
from .forms import LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Login  # imports Login model from models.py
from django.urls import reverse_lazy


class Home(LoginView):
    template_name = "home.html"


class PassCreate(CreateView):
    model = Login
    fields = ["username", "password", "note"]

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

    return render(request, "passwords/index.html", {"passwords": passwords})


def password_detail(request, password_id):
    password = Login.objects.get(id=password_id)
    return render(request, "passwords/detail.html", {"password": password})


def signup(request):
    error_message = ""
    if request.method == "POST":
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect("cat-index")
        else:
            error_message = "Invalid sign up - try again"
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "signup.html", context)
    # Same as:
    # return render(
    #     request,
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )


class PassCreate(CreateView):
    model = Login
    form_class = LoginForm
    template_name = "passwords/index.html"
    success_url = "/passwords"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["passwords"] = Login.objects.all()
        return context


class PasswordUpdate(UpdateView):
    model = Login
    form_class = LoginForm
    template_name = "passwords/index.html"
    success_url = "/passwords/"

    def get(self, request, *args, **kwargs):
        password_id = kwargs.get("pk")

        form = LoginForm
        passwords = Login.objects.all().order_by("id")

        if password_id:
            login_instance = get_object_or_404(self.model, id=password_id)
            form = self.form_class(
                instance=login_instance
            )  # Populate the form with the specific Login object
        else:
            form = self.form_class()
        return render(
            request,
            "passwords/index.html",
            {"passwords": passwords, "updateform": form, "password_id": password_id},
        )


# class PasswordDelete(DeleteView):
#     model = Login
#     success_url = "/passwords/"


class CrudView(View):
    model = Login
    form_class = LoginForm
    template_name = "passwords/index.html"
    success_url = "/passwords"

    def get(self, request, *args, **kwargs):
        password_id = kwargs.get("id")

        form = LoginForm
        passwords = Login.objects.all().order_by("id")

        if password_id:
            login_instance = get_object_or_404(self.model, id=password_id)
            form = self.form_class(
                instance=login_instance
            )  # Populate the form with the specific Login object
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
            login_instance.user = request.user  # Set the logged-in user
            login_instance.save()
            return redirect(self.success_url)
        else:
            print(form.errors)  # Print form errors for debugging
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
        return JsonResponse({'message': 'Password deleted successfully!'}, status=200)



def simple_password_create(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login_instance = form.save(commit=False)
            login_instance.user = request.user
            login_instance.save()
            return redirect("/passwords/")  # Replace with your correct redirect URL
    else:
        form = LoginForm()
    return render(request, "passwords/index.html", {"form": form})
