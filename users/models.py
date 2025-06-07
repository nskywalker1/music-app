from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
	def create_user(self, email, username, password=None, **extra_fields):
		if not email:
			raise ValueError('The email field must be set.')
		email = self.normalize_email(email)
		user = self.model(email=email, username=username, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self, email, username, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
	ROLE_CHOICES = (
		('user', 'User'),
		('artist', 'Artist'),
		('admin', 'Admin')
	)
	username = models.CharField(max_length=150, unique=True)
	email = models.EmailField(unique=True, max_length=50)
	role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
	avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return self.email

class ArtistProfile(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='artist_profile')
	bio = models.TextField(blank=True, null=True)
	followers = models.ManyToManyField(
		CustomUser,
		related_name='subscribed_artists',
		blank=True,
		symmetrical=False
	)