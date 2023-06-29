from django.urls import path
from .views import RegisterUser, login_view, InvalidCode, LogoutViewCustom, Code

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutViewCustom, name='logout'),
    path('signup/', RegisterUser.as_view(), name='signup'),
    path('code/<str:user>', Code.as_view(), name='code'),
    path('code/invalid/', InvalidCode.as_view(), name='invalid_code'),
]