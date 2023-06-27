from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CommonSignupFormView, login_view, GetCode

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/',
         LogoutView.as_view(template_name='sign/templates/logout.html'),
         name='logout'),
    path('signup/',
         CommonSignupFormView.as_view(template_name='sign/templates/signup.html'),
         name='signup'),
    path('code/<str:user>', GetCode.as_view(), name='code'),
]