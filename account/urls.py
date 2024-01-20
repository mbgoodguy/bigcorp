from django.shortcuts import render
from django.urls import path, reverse_lazy

from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    # registration/verification
    path('register/', views.user_register, name='register'),
    path('email-verification-sent/',
         lambda request: render(request, 'account/email/email-verification-sent.html'),
         name='email-verification-sent'
         ),

    # login/logout
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # dashboard
    path('dashboard/', views.dashboard_user, name='dashboard'),
    path('profile_management/', views.profile_user, name='profile-management'),
    path('delete_user/', views.delete_user, name='delete-user'),

    # password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password/password_reset.html',
        email_template_name='account/password/password_reset_email.html',
        success_url=reverse_lazy('account:password-reset-done')),
         name='password-reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password/password_reset_done.html'),
         name='password-reset-done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password/password_reset_confirm.html',
        success_url=reverse_lazy('account:password-reset-complete')),
         name='password-reset-confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password/password_reset_complete.html'),
         name='password-reset-complete'),

]
