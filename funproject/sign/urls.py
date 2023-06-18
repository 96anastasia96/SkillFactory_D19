from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CommonSignupForm, login_view, GetCode

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('signup/',
         CommonSignupForm.as_view(template_name='sign/signup.html'),
         name='signup'),
    path('code/<str:user>', GetCode.as_view(), name='code'),
]