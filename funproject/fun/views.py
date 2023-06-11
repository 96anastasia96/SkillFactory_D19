import values as values
from django.contrib import messages
from django.core.mail import message
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .forms import AnnouncementForm, CommentForm
from .models import Announcement, Comment, Profile

# Create your views here.


def home(request):
    return render(request, 'home.html', {})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("You must be logged in to view this page."))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        ads = Announcement.objects.filter(author_id=pk).order_by("-date_added")

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()


        return render(request, "profile.html", {"profile": profile, "ads": ads})
    else:
        messages.success(request, ("You must be logged in to view this page."))
        return redirect('home')



class AdList(ListView):
    model = Announcement
    ordering = ['-date_added']
    paginate_by = 10
    template_name = 'ads.html'
    context_object_name = 'ads'

    def ads(request):
        ads = Announcement.objects.all()
        context = {'ads': ads}
        return render(request, 'ads.html', context)


class CommentView(ListView):
    model = Comment
    ordering = ['-date']
    paginate_by = 20
    template_name = 'comments_list.html'
    context_object_name = 'comments'

    def comments(request):
        comments = Comment.objects.all()
        ad = Announcement.objects.all()
        context = {'comments': comments, 'ad': ad}
        return render(request, 'comments_list.html', context)


class AdView(DetailView):
    model = Announcement
    template_name = 'ad_view.html'
    context_object_name = 'ad'
    queryset = Announcement.objects.all()
    form = CommentForm

# comments
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            ad = self.get_object()
            form.instance.user = request.user
            form.instance.announcement = ad
            comment = form.save()
            request.user.profile.comments.add(comment)
            return redirect(reverse("ad", kwargs={
                'pk': ad.pk
            }))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        comments = Comment.objects.filter(announcement__author=self.request.user, announcement=self.get_object())
        context["comments"] = comments
        return context

    def add_ad(request):
        submitted = False
        if request.method == "POST":
            form = AnnouncementForm(request.POST, request.FILES)
            if form.is_valid():
                announcement = form.save(commit=False)
                announcement.author = request.user.id
                announcement.save
                return HttpResponseRedirect(reverse('ad', kwargs={'pk': announcement.pk}))
        else:
            form = AnnouncementForm()
            if 'submitted' in request.GET:
                submitted = True
            return render(request, 'ads_form.html', {'form': form, 'submitted': submitted})


class AdCreate(CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'ads_form.html'
    success_url = '/ads/'

    def form_valid(self, form):
        form.instance.author = self.request.user # автором станет текущий пользователь
        return super().form_valid(form)


class AdUpdate(UpdateView):
    model = Announcement
    template_name = 'edit_ad.html'
    fields = ['title', 'text', 'category', 'image', 'video']


class AdDelete(DeleteView):
    model = Announcement
    template_name = 'delete_ad.html'
    success_url = reverse_lazy('ads')


def ad_like(request, pk):
    if request.user.is_authenticated:
        announcement = get_object_or_404(Announcement, id=pk)
        if announcement.likes.filter(id=request.user.id):
            announcement.likes.remove(request.user)
        else:
            announcement.likes.add(request.user)

        return redirect('ads')

    else:
        message.success(request, ("You must be logged in"))
        return redirect('ads')
