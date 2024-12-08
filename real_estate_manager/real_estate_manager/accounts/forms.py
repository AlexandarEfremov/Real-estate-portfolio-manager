from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CustomLoginForm(AuthenticationForm):
    """Custom login form with enhanced error messages."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}),
        error_messages={
            'required': 'Username is required.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        error_messages={
            'required': 'Password is required.',
        }
    )


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with enhanced error handling."""
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages.update({
            'unique': 'This username is already taken.',
            'required': 'Please enter a username.',
        })
        self.fields['password1'].error_messages.update({
            'required': 'Please enter a password.',
        })
        self.fields['password2'].error_messages.update({
            'required': 'Please confirm your password.',
            'password_mismatch': 'The passwords do not match.',
        })
