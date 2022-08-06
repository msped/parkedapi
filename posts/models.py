import uuid
from django.db import models
from users.models import Profile

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    slug = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    image = models.ImageField(upload_to="")
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=140)

    def get_likes_count(self):
        return PostLikes.objects.filter(post=self.id).count()

    def __str__(self):
        return f'{self.image} - {self.created_at}'

    def save(self, *args, **kwargs):
        self.slug = uuid.uuid4()
        super(Post, self).save(*args, **kwargs)

class PostLikes(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile , on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile} - {self.post}'

class Comment(models.Model):
    profile = models.ForeignKey(Profile , on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_likes_count(self):
        return CommentLikes.objects.filter(comment=self.id).count()

    def __str__(self):
        return f'{self.profile} - {self.post}'

class CommentLikes(models.Model):
    comment = models.ForeignKey(Comment , on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile , on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile} - {self.comment}'
