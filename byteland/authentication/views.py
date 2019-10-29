from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext as _

from .forms import RegisterUserForm


class RegisterUserView(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'authentication/register_user.html', {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            # profile = Profile.objects.create(user=new_user)
            # profile.send_activation_code(request)
            messages.success(request,
                             _('Successfully created your account. \
                                for activating it check your email'))
            return HttpResponseRedirect('/')
        else:
            return render(request,
                          'authentication/register_user.html',
                          {'form': form})
