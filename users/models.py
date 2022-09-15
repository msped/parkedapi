from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Profile(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    private_account = models.BooleanField(default=False)
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(max_length=256, null=True, blank=True)
    block_list = models.ManyToManyField('self', symmetrical=False)

    def __str__(self):
        return f"{self.username}'s Profile"

class Followers(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="current_%(class)s_related"
    )
    follower = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="%(class)s_related"
    )

    def __str__(self):
        return f'{self.follower.username} is following {self.user.username}'
