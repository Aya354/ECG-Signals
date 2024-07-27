from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    speciallization = models.TextField(max_length=30, blank=True)
    nationality = models.CharField(max_length=100, default='Egyptian')

    def __str__(self):
        return f"{self.user.username}'s Profile"
