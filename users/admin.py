from django.contrib import admin
from .models import CustomUser, ArtistProfile


class ArtistProfileInline(admin.StackedInline):
    model = ArtistProfile
    extra = 1


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('email', 'username')
    fields = ['username', 'email', 'role']
    list_filter = ('role', 'is_active')
    inlines = (ArtistProfileInline,)
