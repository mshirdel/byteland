import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from byteland.authentication.forms import EditUserForm
from byteland.story.models import Story

from .forms import EditProfileForm


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user_stories = Story.stories.filter(user=request.user)
        paginator = Paginator(user_stories, settings.PAGE_SIZE)
        page = request.GET.get('page')
        try:
            stories = paginator.get_page(page)
        except PageNotAnInteger:
            stories = paginator.get_page(1)
        except EmptyPage:
            stories = paginator(paginator.num_pages)

        return render(request,
                      'user_profile/profile.html',
                      {
                          "stories": stories,
                          "user_stories_count": user_stories.count()}
                      )


@method_decorator(login_required, name='dispatch')
class ProfileEditView(View):
    def get(self, request):
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_profile/edit.html', context)

    def post(self, request):
        user_form = EditUserForm(instance=request.user, data=request.POST)
        profile_form = EditProfileForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was updated")
        # else:
        #     messages.error(request, "Something goes wrong")
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

        return render(request, 'user_profile/edit.html', context)
