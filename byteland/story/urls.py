from django.urls import path

from .views import NewStory, fetch_title

app_name='story'

urlpatterns = [
    path('new/', NewStory.as_view(), name="new_story"),
    path('fetch_title/', fetch_title, name="fetch_title"),
]
