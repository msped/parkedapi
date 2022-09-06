from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Profile(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    private_account = models.BooleanField(default=False)
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(max_length=256, null=True, blank=True)
