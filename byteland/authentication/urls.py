from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterUserView

app_name = 'auth'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', auth_views.LoginView.as_view(
        template_name='authentication/login.html'), name='login')
]
