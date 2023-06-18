from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.db import models


class OneTimeCode(models.Model):
    user = models.CharField(max_length=256)
    code = models.CharField(max_length=10)


class CommonSignupForm(SignupForm):

    class Meta:
        model = User
        fields = ("username",
                  'email',
                  "password1",
                  "password2",)

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

