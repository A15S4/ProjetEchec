"""
Nom du fichier : forms.py
Contexte : Ce fichier définit les formulaires utilisés dans l'application Django, y compris les formulaires de connexion et d'inscription des utilisateurs.
Auteurs : Alexandre Chapleau
"""

from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "input"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input"
            }
        ),
        error_messages={'invalid': "Ce nom d'utilisateur est déjà utilisé"}
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input"
            }
        )
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        password1 = self.cleaned_data.get("password1")
        pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$'
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        if len(password2) < 8:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 8 caractères")
        if not re.match(pattern, password2):
            raise forms.ValidationError("Le mot de passe doit contenir une majuscule, un chiffre et un caractère spécial")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError("L'email doit être au format exemple@exemple.com")
        return email
    
