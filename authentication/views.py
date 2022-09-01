from django import template
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, BadHeaderError, EmailMessage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from main.views import create_user_profile
from .forms import RegisterForm, EditRegisterForm
from .token import account_activation_token


# registration without an activation link

# def register(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             # username = form.cleaned_data.get('username')
#             messages.success(request, 'Your account has been successfully created!')
#         else:
#             messages.error(request, f'Something went wrong!\n\n {form.errors}')
#         return redirect(reverse("authentication:register"))
#
#     else:
#         form = RegisterForm()
#     return render(request, "authentication/register.html", {"register_form": form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Please confirm your email address to complete the registration.'
            message = render_to_string('authentication/active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, 'Activation link has been sent to your email address! Please confirm.')
        else:
            messages.error(request, f'Something went wrong!\n\n {form.errors}')
        return redirect(reverse("authentication:register"))

    else:
        form = RegisterForm()
    return render(request, "authentication/register.html", {"register_form": form})


def activate_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect(reverse("authentication:login_user"))
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def edit_register(request):
    if request.method == 'POST':
        form = EditRegisterForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('main:user_profile')
    else:
        form = EditRegisterForm(instance=request.user)

    return render(request, 'authentication/edit_register.html', {'register_form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('main:home_page')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                create_user_profile(request)
                messages.success(request, f"You've been successfully logged in as {username}!")
                return render(request, 'authentication/login.html')
            else:
                messages.error(request, "Username or password not correct. Try again.")

    return render(request, 'authentication/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You've been successfully logged out!")
    return redirect('authentication:login_user')


# for logged in users
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been changed!')
            return redirect('main:user_profile')
        else:
            return redirect('authentication:change_password')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'authentication/change_password.html', {'register_form': form})


# reset forgot password -logout user
def password_reset(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data) | Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = 'Password Reset Requested'
                    plaintext = template.loader.get_template('authentication/password_reset_email.txt')
                    htmltemp = template.loader.get_template('authentication/password_reset_email.html')
                    content = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'authentication',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    text_content = plaintext.render(content)
                    html_content = htmltemp.render(content)
                    try:
                        msg = EmailMultiAlternatives(subject, text_content, 'yOUR_GMAIL', [user.email],
                                                     headers={'Reply-To': 'YOUR_GMAIL'})
                        msg.attach_alternative(html_content, 'text/html')
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect('authentication:login_user')
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request, 'authentication/password_reset.html', {'password_reset_form': password_reset_form})
