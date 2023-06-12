from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import Avatar
from django.db.models import Q
from .models import Blog
from .forms import BlogRegisterForm
from datetime import date

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=request.user.id)
        except Avatar.DoesNotExist:
            avatar = None
        publicBlogs = Blog.objects.filter(publico=True).order_by('-fecha_creacion')
        privateBlogs = Blog.objects.filter(publico=False).order_by('-fecha_creacion')
        context = {"avatar": avatar, "publicBlogs": publicBlogs, "privateBlogs": privateBlogs}
        return render(request, "home.html", context)
    else:
        return render(request, "home.html")

def about(request):
    return render(request, "about.html", {})

def pages(request):
    blogs = Blog.objects.filter(publico=True).order_by('-fecha_creacion')
    return render(request, "pages.html", {"blogs": blogs})

def detail(request, id):
    try:
        blog = Blog.objects.get(id=id)
        blog.visitas += 1
        blog.save()
        context = {"blog": blog}
        return render(request, "detail.html", context)
    except Blog.DoesNotExist:
       return render(request, "404.html")
    
@login_required
def newBlog(request):
    if request.method == 'POST':
        form = BlogRegisterForm(request.POST)
        if form.is_valid:
                data = form.cleaned_data
                blog = Blog(titulo = data["titulo"],cuerpo = data["cuerpo"], fecha_creacion = date.today(), imagen = data["imagen"], publico = data["publico"], visitas = 0, user = request.user)
                blog.save()
                form = BlogRegisterForm()
                message = "¡Blog creado con éxito!"
                return render(request, "success.html", {"message": message})
    else:
        form = BlogRegisterForm()
    
    return render(request, "new-blog.html", {"form":form})


@login_required  
def editBlog(request, id):
    user = request.user
    try:
        blog = Blog.objects.get(Q(id=id) & Q(user=user))
    except Blog.DoesNotExist:
        return render(request, "404.html")
    
