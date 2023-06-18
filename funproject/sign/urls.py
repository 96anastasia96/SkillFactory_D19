from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CommonSignupForm, login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('signup/',
         CommonSignupForm.as_view(template_name='sign/signup.html'),
         name='signup'),
]