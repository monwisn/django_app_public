from django.urls import path
from django.contrib.auth import views as auth_views

from .views import register, edit_register, login_user, logout_user, change_password, password_reset, activate_email

app_name = 'authentication'
urlpatterns = [
    path('', register, name='register'),
    path('activate/<uidb64>/<token>/', activate_email, name='activate'),
    path('edit-register/', edit_register, name='edit_register'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('change-password/', change_password, name='change_password'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),
         name='password_reset_complete'),
]
