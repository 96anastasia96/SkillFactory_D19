import random
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import CommonSignupForm
from django.shortcuts import render


def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            OneTimeCode.objects.create(code=random.choice('abcde'), user=user)
        else:
            error_message = 'Invalid username or password'
    return render(request, 'sign/login.html', {'error_message': error_message})


def login_with_code_view(request):
    username = request.POST['username']
    code = request.POST['code']
    if OneTimeCode.objects.filter(code=code, user__username=username).exists():
        login(request, user)
    else:
        error_message = 'Invalid code. Try again.'


class CommonSignupForm(CreateView):
    model = User
    form_class = CommonSignupForm
    success_url = '/'



