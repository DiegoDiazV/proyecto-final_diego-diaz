from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('about', views.about, name="About"),
    path('pages', views.pages, name="Pages"),
    path('pages/<id>', views.detail, name="Detail"),
    path('new-blog', views.newBlog, name="NewBlog")
]