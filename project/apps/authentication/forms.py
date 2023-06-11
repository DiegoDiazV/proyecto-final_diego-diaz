from django import forms
from .models import Avatar
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label="Apellido", widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]
        help_texts = {k: "" for k in fields}

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label="Apellido", widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

class AvatarForm(forms.Form):
    imagen = forms.ImageField(label="imagen") 
    class Meta:
        model = Avatar
        fields = ["imagen"]
