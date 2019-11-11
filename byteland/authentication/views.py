from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.views import View

from .forms import RegisterUserForm, ResendEmailActivationForm
from .models import User
from .tokens import user_email_activation_token
from .utils import send_activation_email


class JoinUserView(View):
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
            send_activation_email(request, new_user)

            # TODO add profile app
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


class UserEmailActivationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (ValueError, TypeError, BufferError, User.DoesNotExist):
            user = None
        if user is not None and user_email_activation_token.check_token(user, token):
            user.email_confirmed = True
            user.is_active = True
            user.save()
            messages.success(request, _(
                'Yout email has been verified. You can login now'))
            return render(request, 'authentication/email_activation.html', {
                'show_login': True
            })
        else:
            messages.error(request, _(
                'There was problem for activation email.'))
            return render(request, 'authentication/email_activation.html', {
                'show_resend_activation_code': True
            })


class ResendEmailActivationCodeView(View):
    def get(self, request):
        form = ResendEmailActivationForm()
        return render(request, 'authentication/resend_email_activation_code.html',
                      {'form': form})

    def post(self, request):
        form = ResendEmailActivationForm(request.POST)
        if form.is_valid():
            try:
                email_for_activation = form.cleaned_data['email']
                user = User.objects.get(email=email_for_activation)
                if not user.email_confirmed:
                    send_activation_email(request, user)
                    messages.success(request, _(
                        'Please check your email. We sent an activation link'))
                    return HttpResponseRedirect('/')
                else:
                    messages.info(request, _(
                        'Yout email has been verified before.'))
                    return HttpResponseRedirect('/')
            except User.DoesNotExist:
                messages.error(request, _(
                    f'There is not any user with this email: {email_for_activation}.'))
                return HttpResponseRedirect('/')
        else:
            messages.error(request, _('Please enter your email'))
            return HttpResponseRedirect('/')
