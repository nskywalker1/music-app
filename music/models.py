from django.db import models
from users.models import CustomUser


class Album(models.Model):
    artist = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='album_covers/', blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.artist}'

    class Meta:
        verbose_name_plural = 'Albums'
        verbose_name = 'Album'
        ordering = ['title']


class Track(models.Model):
    artist = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tracks')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, related_name='tracks', null=True, blank=True)
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='tracks/', blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    cover = models.ImageField(upload_to='track_covers/', blank=True, null=True)
    plays_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title} - {self.artist}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.audio_file:
            from mutagen import File as MutagenFile
            audio = MutagenFile(self.audio_file.path)
            if audio and audio.info:
                from datetime import timedelta
                self.duration = timedelta(seconds=int(audio.info.length))
                super().save(update_fields=['duration'])

    class Meta:
        verbose_name_plural = 'Tracks'
        verbose_name = 'Track'
        indexes = [models.Index(fields=['artist', 'title'])]


class Playlist(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='playlist_covers/', blank=True, null=True)
    tracks = models.ManyToManyField(Track, related_name='playlists', blank=True)

    def __str__(self):
        return f'{self.name} - {self.owner}'

    class Meta:
        verbose_name_plural = 'Playlists'
        verbose_name = 'Playlist'
