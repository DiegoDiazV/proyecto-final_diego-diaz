from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import Avatar
from django.db.models import Q
from .models import Blog, Comentario
from .forms import BlogForm, ComentarioForm, SearchBlogForm
from django.utils import timezone

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(user=request.user.id)
        except Avatar.DoesNotExist:
            avatar = None
        publicBlogs = Blog.objects.filter(Q(publico=True) & Q(user=request.user)).order_by('-fecha_creacion')
        privateBlogs = Blog.objects.filter(Q(publico=False) & Q(user=request.user)).order_by('-fecha_creacion')
        context = {"avatar": avatar, "publicBlogs": publicBlogs, "privateBlogs": privateBlogs}
        return render(request, "home.html", context)
    else:
        return render(request, "home.html")

def about(request):
    return render(request, "about.html", {})

def pages(request):
    if request.method == 'POST':
        form = SearchBlogForm(request.POST)
        print(form)
        if form.is_valid:
            data = form.cleaned_data
            blogs = Blog.objects.filter(Q(publico=True) & Q(titulo__contains = data['search_text'])).order_by('-fecha_creacion')
            form = SearchBlogForm()
            render(request, "pages.html", {"blogs": blogs, "form": form})
    else:
        form = SearchBlogForm()
        blogs = Blog.objects.filter(publico=True).order_by('-fecha_creacion')
    return render(request, "pages.html", {"blogs": blogs, "form": form})

def detail(request, id):
    try:
        blog = Blog.objects.get(id=id)
        blog.visitas += 1
        blog.save()
        comentarios = Comentario.objects.filter(blog = blog).order_by('-fecha_creacion')
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = ComentarioForm(request.POST)
                print(form)
                if form.is_valid:
                    data = form.cleaned_data
                    comentario = Comentario(comentario = data["comentario"], fecha_creacion = timezone.now(), user = request.user, blog = blog)
                    comentario.save()
                    form = ComentarioForm()
                    message = "¡Comentario agregado con éxito!"
                    return render(request, "success.html", {"message": message})
            else:
                form = ComentarioForm()
            context = {"blog": blog, "comentarios": comentarios, "form": form}
            return render(request, "detail.html", context)
        else:
            context = {"blog": blog, "comentarios": comentarios,}
            return render(request, "detail.html", context)
    except Blog.DoesNotExist:
       return render(request, "404.html")
    
@login_required
def newBlog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        print(form)
        if form.is_valid:
            data = form.cleaned_data
            blog = Blog(titulo = data["titulo"],cuerpo = data["cuerpo"], fecha_creacion = timezone.now(), imagen = data["imagen"], publico = data["publico"], visitas = 0, user = request.user)
            blog.save()
            form = BlogForm()
            message = "¡Blog creado con éxito!"
            return render(request, "success.html", {"message": message})
    else:
        form = BlogForm()
    
    return render(request, "new-blog.html", {"form":form})


@login_required  
def editBlog(request, id):
    user = request.user
    try:
        blog = Blog.objects.get(Q(id=id) & Q(user=user))
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)
            print(form)
            if form.is_valid:
                data = form.cleaned_data
                blog.titulo = data["titulo"]
                blog.cuerpo = data["cuerpo"]
                if data["imagen"] != None:
                    blog.imagen = data["imagen"]
                blog.publico = data["publico"]
                blog.save()
                message = "¡Blog editado con éxito!"
                return render(request, "success.html", {"message": message})
        else:
            form = BlogForm(initial={"titulo": blog.titulo, 'cuerpo': blog.cuerpo, 'imagen': blog.imagen, 'publico': blog.publico})
        
        return render(request, "edit-blog.html", {"form": form, "blog_id":id})
    except Blog.DoesNotExist:
        return render(request, "404.html")
    
@login_required  
def deleteBlog(request, id, fromDetail):
    user = request.user
    try:
        if user.is_staff:
            blog = Blog.objects.get(id=id)
        else:
            blog = Blog.objects.get(Q(id=id) & Q(user=user))
        if request.method == 'POST':
            blog.delete()
            message = "¡Blog eliminado con éxito!"
            return render(request, "success.html", {"message": message})
        else:
            return render(request, "delete-blog.html", {"blog": blog, "fromDetail": fromDetail})
    except Blog.DoesNotExist:
        return render(request, "404.html")
    
@login_required  
def deleteComment(request, id):
    user = request.user
    try:
        comentario = Comentario.objects.get(Q(id=id) & Q(user=user))
        if request.method == 'POST':
            comentario.delete()
            message = "¡Comentario eliminado con éxito!"
            return render(request, "success.html", {"message": message})
        else:
            return render(request, "delete-comment.html", {"comentario": comentario})
    except Comentario.DoesNotExist:
        return render(request, "404.html")
    
@login_required 
def unpublishBlog(request, id):
    user = request.user
    if user.is_staff:
        try:
            blog = Blog.objects.get(id = id)
            if request.method == 'POST':
                blog.publico = False
                blog.save()
                message = "¡Blog despublicado con éxito!"
                return render(request, "success.html", {"message": message})
            else:
                return render(request, "unpublish-blog.html", {"blog": blog})
        except Blog.DoesNotExist:
            return render(request, "404.html")
    else:
        return render(request, "404.html")

