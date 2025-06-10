from django.shortcuts import render, redirect
from .models import CustomUser, ArtistProfile
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('role') == 'artist':
                ArtistProfile.objects.create(user=user, bio=form.cleaned_data.get('bio'))
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})
