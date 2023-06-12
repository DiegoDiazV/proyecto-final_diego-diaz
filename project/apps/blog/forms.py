from django import forms
from .models import Blog

class BlogRegisterForm(forms.Form):
    titulo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    cuerpo = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    publico = forms.BooleanField(label="¿Público?", initial=False, widget=forms.CheckboxInput(attrs={'class':'form-control'}))
    imagen = forms.ImageField(label="imagen")

    class Meta:
        model = Blog
        field = ['titulo', 'cuerpo', 'publico', 'imagen']