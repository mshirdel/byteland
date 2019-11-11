from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (JoinUserView, UserEmailActivationView,
                    ResendEmailActivationCodeView)

app_name = 'auth'

urlpatterns = [
    path('join/',
         JoinUserView.as_view(),
         name='register_user'),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='authentication/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(next_page='/'),
         name='logout'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             success_url='/auth/password_reset_done'),
         name='password_reset'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url='/auth/reset/done'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('activation/email/<uidb64>/<token>/',
         UserEmailActivationView.as_view(), name='account_activation_confirm'),
    path('activation/resend/',
         ResendEmailActivationCodeView.as_view(),
         name='resend_email_activation')
]
