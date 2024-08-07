from django import forms
from .models import Login
from django.contrib.auth.hashers import make_password


class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ["appname", "username", "password", "note"]

        def save(self):
            logininfo = super().save()
            logininfo.password = make_password(
                self.cleaned_data["password1"],
                hasher="main_app.hashers.MyBCryptSHA256PasswordHasher",
            )  # Set the password manually with custom hasher

            logininfo.save()
            return logininfo
