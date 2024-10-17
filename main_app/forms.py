from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from .models import Login

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Password',
        })    


class LoginEntryForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ["appname", "username", "password", "note"]

    def save(self, commit=True):
        login_instance = super().save(commit=False)
        login_instance.password = make_password(self.cleaned_data["password"])
        if commit:
            login_instance.save()
        return login_instance
        
class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        form_id = kwargs.pop('form_id', '')
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'username',
            'id': f'username-{form_id}',  # Use the dynamic form_id
            'type': 'text',
            'placeholder': 'John Doe',
            'maxlength': '16',
            'minlength': '6',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'email',
            'id': f'email-{form_id}',  # Use the dynamic form_id
            'type': 'email',
            'placeholder': 'JohnDoe@mail.com',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'password1',
            'id': f'password1-{form_id}',  # Use the dynamic form_id
            'type': 'password',
            'placeholder': 'password',
            'maxlength': '22',
            'minlength': '8',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'password2',
            'id': f'password2-{form_id}',  # Use the dynamic form_id
            'type': 'password',
            'placeholder': 'password',
            'maxlength': '22',
            'minlength': '8',
        })

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']
