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
            user.is_active = False  # Добавьте эту строку
            user.save()  # Сохраните пользователя после добавления is_active

            send_email(user)

            return redirect('account:email-verification-sent')

    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form})


def email_verification():
    return None
