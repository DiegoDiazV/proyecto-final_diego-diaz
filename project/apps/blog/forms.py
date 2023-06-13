from django import forms
from .models import Blog

class BlogForm(forms.Form):
    titulo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    cuerpo = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    publico = forms.BooleanField(label="¿Público?", initial=False, required=False, widget=forms.CheckboxInput(attrs={'class':''}))
    imagen = forms.ImageField(label="imagen",  required=False)

    class Meta:
        model = Blog
        field = ['titulo', 'cuerpo', 'publico', 'imagen']