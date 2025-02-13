from django.shortcuts import render
from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm

# Create your views here.
def profiles(request):
    return render(request, 'users/profiles.html')

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('index')

        else:
            messages.success(
                request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)
