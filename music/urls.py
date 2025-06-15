from django.urls import path
from .views import track_create_view

app_name = 'music'

urlpatterns = [
    path('track/create/', track_create_view, name='track_create'),
]