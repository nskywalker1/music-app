from django.shortcuts import render, redirect
from .models import CustomUser, ArtistProfile
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, authenticate, logout


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('role'))
            user = form.save()
            if form.cleaned_data.get('role') == 'artist':
                ArtistProfile.objects.create(user=user, bio=form.cleaned_data.get('bio'))
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})
