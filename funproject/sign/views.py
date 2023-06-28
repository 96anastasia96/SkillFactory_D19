import random
from string import digits
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic.edit import CreateView
from funproject import settings
from .models import OneTimeCode
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:  # Проверка активности пользователя
            login(request, user)
            messages.success(request, ("You Have Been Logged In!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in. Please Try Again..."))
            return redirect('login')

    else:
        return render(request, "sign/templates/login.html", {})


def verify_code(request):
    if request.method == "POST":
        code = request.POST['code']
        if OneTimeCode.objects.filter(code=code, user=request.user).exists() and request.user.is_active:  # Проверка активности пользователя
            User.objects.filter(username=request.user.username).update(is_active=True)
            OneTimeCode.objects.filter(code=code, user=request.user).delete()
            messages.success(request, ("Code verification successful. You can now login."))
            return redirect('login')
        else:
            messages.error(request, ("Invalid code or user is not active. Please try again."))
            return redirect('verify_code')

    return render(request, "sign/templates/code.html", {})


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            code = ''.join(random.choices(digits, k=6))
            one_time_code = OneTimeCode(user=user, code=code)  # Указываем пользователя при создании объекта
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
            user = authenticate(username=username, password=password)

            messages.success(request, ("Код был отправлен на вашу почту."))
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
            context['message'] = "Код был отправлен на вашу почту."
        return context


class InvalidCode(CreateView):
    template_name = 'sign/templates/invalid_code.html'


def LogoutViewCustom(request):
        logout(request)
        messages.success(request, ("You Have Been Logged Out."))
        return redirect('home')
