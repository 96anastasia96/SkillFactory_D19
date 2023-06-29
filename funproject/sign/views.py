import random
from string import hexdigits
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
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


class RegisterUser(CreateView):
    model = User
    template_name = 'sign/templates/signup.html'
    form_class = SignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SignUpForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
        return redirect('code', request.POST['username'])


class Code(CreateView):
    template_name = 'sign/templates/code.html'

    def get_context_data(self, **kwargs):
        name_user = self.kwargs.get('user')
        if not OneTimeCode.objects.filter(user=name_user).exists():
            code = ''.join(random.sample(hexdigits, 6))
            OneTimeCode.objects.create(user=name_user, code=code)
            user = User.objects.get(username=name_user)
            # Отправка почты с OTP-кодом
            send_mail(
                subject='Код активации',
                message=f'Ваш код активации: {code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = request.path.split('/')[-1]
            if OneTimeCode.objects.filter(code=request.POST['code'], user=user).exists():
                User.objects.filter(username=user).update(is_active=True)
                OneTimeCode.objects.filter(code=request.POST['code'], user=user).delete()
            else:
                return render(self.request, 'sign/templates/invalid_code.html')
        return redirect('login')


class InvalidCode(CreateView):
    template_name = 'sign/templates/invalid_code.html'


def LogoutViewCustom(request):
        logout(request)
        messages.success(request, ("You Have Been Logged Out."))
        return redirect('home')
