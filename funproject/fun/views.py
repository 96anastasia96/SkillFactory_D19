from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Announcement, Category
# Create your views here.


class AdList(ListView):
    model = Announcement
    paginate_by = 10
    template_name = 'ads.html'
    context_object_name = 'ads'


    def ads(request):
        ads = Announcement.objects.all()
        context = {'ads': ads}
        return render(request, 'ads.html', context)


class AdView(DetailView):
    model = Announcement
    queryset = Announcement.objects.all()


class AdCreate(CreateView):
    model = Announcement


class AdUpdate(UpdateView):
    model = Announcement


class AdDelete(DeleteView):
    model = Announcement
