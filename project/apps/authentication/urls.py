from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_request, name="Login"),
    path('signup', views.signup, name="Signup"),
    path('profile', views.profile, name="Profile"),
    path('profile/avatar', views.avatar, name="Avatar"),
    path('logout', views.CustomLogoutView.as_view(), name= "Logout"),
]