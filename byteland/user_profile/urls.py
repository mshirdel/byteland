from django.urls import path

from .views import ProfileView, ProfileEditView


app_name = 'user_profile'
urlpatterns = [
    ###################
    # PROFILE         #
    ###################

    path('', ProfileView.as_view(), name='profile'),
    path('edit/', ProfileEditView.as_view(),
         name='profile_edit'),
]
