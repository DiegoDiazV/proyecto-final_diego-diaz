from django.shortcuts import redirect
from django.shortcuts import render
from authentication.models import Avatar
from .models import Blog

# Create your views here.
def home(request):
    try:
        avatar = Avatar.objects.get(user=request.user.id)
    except Avatar.DoesNotExist:
        avatar = None

    return render(request, "home.html", {"avatar": avatar})

def about(request):
    return render(request, "about.html", {})

def pages(request):
    blogs = Blog.objects.filter(publico=True)
    return render(request, "pages.html", {"blogs": blogs})