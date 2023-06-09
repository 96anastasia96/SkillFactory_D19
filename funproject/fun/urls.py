from django.urls import path
from .views import (AdList)

urlpatterns = [
    path('ads/', AdList.as_view()),
]
