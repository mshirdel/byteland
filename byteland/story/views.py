import requests
from bs4 import BeautifulSoup
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse

from .forms import StoryForm


@method_decorator(login_required, name='dispatch')
class NewStory(PermissionRequiredMixin, View):
    # 'stories.add_story'
    permission_required = []

    def get(self, request):
        form = StoryForm()
        return render(request, 'story/new.html', {'form': form})

    def post(self, request):
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            form.save_m2m()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'story/new.html', {'form': form})


def fetch_title(request):
    url = request.GET.get('url', None)
    if url is not None:
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            return JsonResponse({'title': soup.title.text})
        else:
            return JsonResponse({'error': 'fetch title not work'})
    else:
        return JsonResponse({'error': 'url not found'})
