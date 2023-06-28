from django.urls import path
from .views import register_user, login_view, InvalidCode, LogoutViewCustom, verify_code, GetCode

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutViewCustom, name='logout'),
    path('signup/', register_user, name='signup'),
    path('code/<str:user>', GetCode.as_view(), name='code'),
    path('code/invalid/', InvalidCode.as_view(), name='invalid_code'),
    path('verify_code/', verify_code, name='verify_code'),
]