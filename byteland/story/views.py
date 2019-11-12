import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from django.conf import settings
from django.db.models import Count
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import StoryForm, StoryCommentForm
from .models import Story, StoryPoint


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


@login_required()
def upvote_story(request, id):
    result_url = '/'
    if request.GET.get('page'):
        result_url = f"/?page={request.GET.get('page')}"
    story = get_object_or_404(Story, pk=id)
    try:
        StoryPoint.objects.get(user=request.user, story=story)
        return HttpResponseRedirect(result_url)
    except StoryPoint.DoesNotExist:
        story_point = StoryPoint(user=request.user, story=story)
        story_point.save()
        return HttpResponseRedirect(result_url)


@login_required()
def downvote_stroy(request, id):
    result_url = '/'
    if request.GET.get('page'):
        result_url = f"/?page={request.GET.get('page')}"
    try:
        story_point = StoryPoint.objects.get(user=request.user, story_id=id)
        story_point.delete()
    except StoryPoint.DoesNotExist:
        pass
    return HttpResponseRedirect(result_url)


class BaseStoryListView(ListView):
    queryset = Story.stories.order_by('-number_of_votes')
    context_object_name = 'stories'
    paginate_by = settings.PAGE_SIZE
    template_name = 'story/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voted_story_ids = []
        if self.request.user.is_authenticated:
            for point in self.request.user.storypoint_set.all():
                voted_story_ids.append(point.story_id)
        context['voted_story_id'] = voted_story_ids
        return context


class TopStoryListView(BaseStoryListView):
    def get_queryset(self):
        return Story.stories.order_by('-number_of_votes')


class LatestStoryListView(BaseStoryListView):
    def get_queryset(self):
        return Story.stories.order_by('-created')


class ByDomainStoryListView(BaseStoryListView):
    def get_queryset(self):
        query_set = super().get_queryset()
        if self.request.GET.get('url'):
            url = self.request.GET.get('url')
            return query_set.filter(url_domain_name=url)
        return query_set


@method_decorator(login_required, name='dispatch')
class EditStory(View):
    def get(self, request, id):
        story = get_object_or_404(Story, pk=id)
        form = StoryForm(instance=story)
        return render(request, 'story/edit.html',
                      {'form': form, 'id': id})

    def post(self, request, id):
        story = get_object_or_404(Story, pk=id)
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            story.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'story/edit.html',
                          {'form': form, 'id': id})


class ShowStory(View):
    def get(self, request, id):
        story = get_object_or_404(Story, pk=id)
        story_comment_form = StoryCommentForm()
        return render(request, 'story/show.html',
                      {
                          'story': story,
                          'form': story_comment_form
                      })

    def post(self, request, id):
        story = get_object_or_404(Story, pk=id)
        if request.user.is_authenticated:
            form = StoryCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.commenter = request.user
                comment.story = story
                comment.save()
                return render(request, 'story/show.html',
                              {'story': story, 'form': StoryCommentForm})
            else:
                return render(request, 'story/show.html',
                              {'story': story, 'form': form})
        else:
            form = StoryCommentForm()
            messages.add_message(request,
                                 messages.WARNING,
                                 _('Please Register to site for commenting')
                                 )
            return render(request, 'story/show.html',
                          {'story': story, 'form': form})
