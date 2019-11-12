from django.urls import path

from .views import (NewStory, fetch_title, TopStoryListView,
                    LatestStoryListView, ByDomainStoryListView,
                    EditStory, ShowStory,
                    upvote_story, downvote_stroy)
from byteland.views import sudo_view

app_name = 'story'

urlpatterns = [
    path('new/', NewStory.as_view(), name="new_story"),
    path('<int:id>/', ShowStory.as_view(), name="show_story"),
    path('fetch_title/', fetch_title, name="fetch_title"),
    path('edit/<int:id>/', EditStory.as_view(), name="edit_story"),
    path('down/<int:id>/', downvote_stroy, name="downvote_story"),
    path('up/<int:id>/', upvote_story, name="upvote_story"),
    path('by/domain/', ByDomainStoryListView.as_view(), name="stories_by_domain"),
    path('latest/', LatestStoryListView.as_view(), name="latest_stories")
]
