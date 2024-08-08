from django import forms
from .models import Login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


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

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'username', 
            'id':'username', 
            'type':'text', 
            'placeholder':'John Doe', 
            'maxlength': '16', 
            'minlength': '6', 
            }) 
        self.fields['email'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'email', 
            'id':'email', 
            'type':'email', 
            'placeholder':'JohnDoe@mail.com', 
            }) 
        self.fields['password1'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'password1', 
            'id':'password1', 
            'type':'password', 
            'placeholder':'password', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
        self.fields['password2'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'password2', 
            'id':'password2', 
            'type':'password', 
            'placeholder':'password', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 


    username = forms.CharField(max_length=20, label=False) 
    email = forms.EmailField(max_length=100) 
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']  # Add any additional fields you want to include in the form