from django.contrib import admin
from .models import CustomUser, ArtistProfile

admin.site.register(CustomUser)
admin.site.register(ArtistProfile)