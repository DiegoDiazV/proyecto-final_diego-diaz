from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import forms, models

# Create your views here.
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect("/")
            else:
                message = "Usuario o contraseña no válidos"
                return render(request, "login.html", {"form": form, "message": message})
        else:
            message = "Usuario o contraseña no válidos"
            return render(request, "login.html", {"form": form, "message": message})
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def signup(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            message = "¡Usuario creado con éxito!"
            return render(request, "success.html", {"message": message})
    else:
        form = forms.UserRegisterForm()

    return render(request, "signup.html", {"form": form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = forms.UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            message = "¡Usuario actualizado con éxito!"
            context = {'form': form, 'message': message}
            return render(request, 'profile.html', context)
    else:
        form = forms.UserUpdateForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'profile.html', context)

@login_required
def avatar(request):
    if (request.method == 'POST'):
        form = forms.AvatarForm(request.POST, request.FILES)
        if form.is_valid:
            print(form)
            u = User.objects.get(username = request.user)
            try:
                avatar = models.Avatar.objects.get(user = u)
                avatar.imagen = form.cleaned_data['imagen']
                avatar.actualizaciones += 1
            except models.Avatar.DoesNotExist:
                avatar = models.Avatar(user = u, imagen = form.cleaned_data['imagen'])
            
            avatar.save()
            message = "¡Usuario actualizado con éxito!"
            context = {'form': form, 'avatar': avatar, 'message': message}
            return render(request, "avatar.html", context)
        
    else:
        form = forms.AvatarForm()
        u = User.objects.get(username = request.user)
        try:
            avatar = models.Avatar.objects.get(user = u)
        except models.Avatar.DoesNotExist:
            avatar = None

    context = {'form': form, 'avatar': avatar}
    return render(request, 'avatar.html', context)

class CustomLogoutView(LogoutView):
    next_page = '/'




