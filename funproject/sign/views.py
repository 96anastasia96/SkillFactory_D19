import random
from string import hexdigits
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.generic.edit import CreateView
from funproject import settings
from .models import CommonSignupForm, OneTimeCode
from django.shortcuts import render, redirect


def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

    return render(request, 'sign/templates/login.html', {'error_message': error_message})



class CommonSignupFormView(CreateView):
    model = User
    form_class = CommonSignupForm
    success_url = '/'
    template_name = 'sign/templates/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommonSignupForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
        return redirect('code', request.POST['username'])


class GetCode(CreateView):
    template_name = 'sign/templates/code.html'

    def get_context_data(self, **kwargs):
        name_user = self.kwargs.get('user')
        if not OneTimeCode.objects.filter(user=name_user).exists():
            code = ''.join(random.sample(hexdigits, 6))
            one_time_code = OneTimeCode(user=name_user, code=code)
            one_time_code.save()
            user = User.objects.get(username=name_user)
            send_mail(
                subject=f'Код активации',
                message=f'Код активации аккаунта: {code}',
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


