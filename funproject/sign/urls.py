from django.urls import path
from .views import CommonSignupFormView, login_view, GetCode, InvalidCode, LogoutViewCustom

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutViewCustom.as_view(), name='logout'),
    path('signup/',
         CommonSignupFormView.as_view(template_name='sign/templates/signup.html'),
         name='signup'),
    path('code/<str:user>', GetCode.as_view(), name='code'),
    path('code/invalid/', InvalidCode.as_view(), name='invalid_code'),
]