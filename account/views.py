from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django_email_verification import send_email

from .forms import UserCreateForm


# Create your views here.
def user_register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')

            user = User.objects.create_user(
                username=user_username, email=user_email, password=user_password
            )

            user.is_active = False

            send_email(user)

            return redirect('')

    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form})


def email_verification():
    return None
