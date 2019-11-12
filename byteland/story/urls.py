from django.contrib.sitemaps.views import sitemap
from django.urls import path

from .feeds import LatesStoryFeed
from .sitemaps import StorySitemap
from .views import (ByDomainStoryListView, EditStory, LatestStoryListView,
                    NewStory, ShowStory, TopStoryListView, downvote_stroy,
                    fetch_title, story_search, upvote_story)

app_name = 'story'

sitemaps = {
    'stories': StorySitemap
}

urlpatterns = [
    path('new/', NewStory.as_view(), name="new_story"),
    path('<int:id>/', ShowStory.as_view(), name="show_story"),
    path('fetch_title/', fetch_title, name="fetch_title"),
    path('edit/<int:id>/', EditStory.as_view(), name="edit_story"),
    path('down/<int:id>/', downvote_stroy, name="downvote_story"),
    path('up/<int:id>/', upvote_story, name="upvote_story"),
    path('by/domain/', ByDomainStoryListView.as_view(), name="stories_by_domain"),
    path('latest/', LatestStoryListView.as_view(), name="latest_stories"),
    path('search/', story_search, name="story_search"),
    path('feed/', LatesStoryFeed(), name="story_feed"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.view.sitemap'),
]
