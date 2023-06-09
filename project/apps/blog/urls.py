from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('about', views.about, name="About"),
    path('pages', views.pages, name="Pages"),
    path('pages/<id>', views.detail, name="Detail"),
    path('user/pages/new', views.newBlog, name="NewBlog"),
    path('user/pages/edit/<id>', views.editBlog, name="EditBlog"),
    path('user/pages/delete/<id>/<fromDetail>', views.deleteBlog, name="DeleteBlog"),
    path('comment/delete/<id>', views.deleteComment, name="DeleteComment"),
    path('pages/unpublish/<id>', views.unpublishBlog, name="UnpublishBlog")
]