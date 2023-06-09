from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView

urlpatterns = [
    path('accounts/login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('accounts/logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('accounts/signup/',
         BaseRegisterView.as_view(template_name='sign/signup.html'),
         name='signup'),

]