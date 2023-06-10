from django.urls import path
from . import views
from .views import (AdList, AdCreate, AdView, CommentView, profile_list, home)

urlpatterns = [
    path('ads/', AdList.as_view(), name='ads'),
    path('ads_form/', AdCreate.as_view(), name='ads_form'),
    path('ad/<int:pk>/', AdView.as_view(), name='ad'),
    path('ad_like/<int:pk>/', views.ad_like, name='ad_like'),
    path('comments/', CommentView.as_view(), name='comments'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('home/', home, name='home'),
    path('profile/<int:pk>', views.profile, name='profile'),

]
