from django.shortcuts import render, redirect
from .forms import TrackForm


def track_create_view(request):
    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.artist = request.user
            track.save()
            return redirect('/')
    else:
        form = TrackForm()
    return render(request, 'music/track_form.html', {
        'form': form
    })
