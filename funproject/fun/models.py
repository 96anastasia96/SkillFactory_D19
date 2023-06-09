from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.name.title()}'


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
   # date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

