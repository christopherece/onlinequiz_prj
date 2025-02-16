from django.shortcuts import render
from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from django.db.models import Q
from .models import Profile, Message
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm

# Create your views here.
def profiles(request):
    return render(request, 'users/profiles.html')

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('quiz')

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
            return redirect(request.GET['next'] if 'next' in request.GET else 'quiz')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login.html')


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
            return redirect('quiz')

        else:
            messages.success(
                request, 'Username is already taken')

    context = {'page': page, 'form': form}
    return render(request, 'users/register.html', context)

@login_required(login_url='login')
def userAccount(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated

    # Get the profile for the current user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Bind the form to the submitted data and files
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save the profile data
            profile = form.save(commit=False)

            # Ensure the associated User object has a username
            if not profile.user.username:
                profile.user.username = profile.username  # Use email as username
                profile.user.save()

            # Save the profile
            profile.save()
            return redirect('account')  # Redirect to a success page
    else:
        # Pre-fill the form with the existing profile data
        form = ProfileForm(instance=profile)

    # Render the form template with the form and profile data
    context = {'form': form, 'profile': profile}
    return render(request, 'users/profiles.html', context)

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
