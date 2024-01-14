from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django_email_verification import send_email

from .forms import UserCreateForm, LoginForm, UserUpdateForm


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


def login_user(request):
    form = LoginForm

    if request.user.is_authenticated:
        return redirect('shop:products')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account:dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect('account:login')

    context = {
        'form': form,
    }

    return render(request, 'account/login/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('shop:products')


@login_required(login_url='account:login')
def delete_user(request):
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.delete()
        return redirect('shop:products')

    return render(request, 'account/dashboard/account_delete.html')


@login_required(login_url='account:login')
def dashboard_user(request):
    return render(request, 'account/dashboard/dashboard.html')


@login_required(login_url='account:login')
def profile_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('account:dashboard')

    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form
    }

    return render(request, 'account/dashboard/profile_management.html', context)

