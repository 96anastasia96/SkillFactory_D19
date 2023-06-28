import random
from string import hexdigits, digits
from allauth.account.views import LogoutView
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.generic.edit import CreateView
from funproject import settings
from .models import OneTimeCode
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Logged In!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in. Please Try Again..."))
            return redirect('login')

    else:
        return render(request, "sign/templates/login.html", {})



def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            code = ''.join(random.choices(digits, k=6))
            one_time_code = OneTimeCode(user=user, code=code)
            one_time_code.save()
            # Отправка почты с OTP-кодом
            send_mail(
                subject='Код активации',
                message=f'Ваш код активации: {code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # email = form.cleaned_data['email']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have successfully registered! Welcome!"))
            return redirect('code', user=user.username)
    return render(request, 'sign/templates/signup.html', {'form': form})


class GetCode(CreateView):
    template_name = 'sign/templates/code.html'
    model = OneTimeCode
    fields = ['code']

    def get_queryset(self):
        return OneTimeCode.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name_user = self.kwargs.get('user')
        if not OneTimeCode.objects.filter(user=User.objects.get(username=name_user)).exists():
            code = ''.join(random.sample(digits, k=6))
            one_time_code = OneTimeCode(user=name_user, code=code)
            one_time_code.save()
            user = User.objects.get(username=name_user)
            send_mail(
                subject=f'Код активации',
                message=f'Код активации аккаунта: {code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            context['message'] = "Код был отправлен на вашу почту."
        return context

    def post(self, request, *args, **kwargs):
        if OneTimeCode.objects.filter(code=request.POST['code'], user=request.user).exists():
            User.objects.filter(username=request.user.username).update(is_active=True)
            OneTimeCode.objects.filter(code=request.POST['code'], user=request.user).delete()
            return redirect('login')
        else:
            return render(self.request, 'sign/templates/invalid_code.html')


class InvalidCode(CreateView):
    template_name = 'sign/templates/invalid_code.html'


def LogoutViewCustom(request):
        logout(request)
        messages.success(request, ("You Have Been Logged Out."))
        return redirect('home')
