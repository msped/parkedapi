from django.db.models.signals import post_save
from notifications.signals import notify
from users.models import Profile

from .models import Comment, CommentLikes, Post, PostLikes

def post_like(sender, instance, **kwargs):
    post = Post.objects.get(id=instance.id)
    profile = Profile.objects.get(id=instance.profile.id)
    recipient = Profile.objects.get(id=instance.author.id)
    notify.send(
        sender=profile,
        recipient=recipient,
        target=post,
        text=f'{profile.username} has liked your post.'
    )

def comment_like(sender, instance, **kwargs):
    comment = Comment.objects.get(id=instance.comment.id)
    profile = Profile.objects.get(id=instance.profile.id)
    recipient = Profile.objects.get(id=instance.comment.profile.id)
    notify.send(
        sender=profile,
        recipient=recipient,
        target=comment,
        text=f'{profile.username} liked your comment.'
    )

def comment_notification(sender, instance, **kwargs):
    comment = Comment.objects.get(id=instance.id)
    profile = Profile.objects.get(id=instance.profile.id)
    recipient = Profile.objects.get(id=instance.post.author.id)
    notify.send(
        sender=profile,
        recipient=recipient,
        target=comment,
        text=f'{profile.username} has commented on your post: "{instance.content}"'
    )

post_save.connect(
    post_like,
    sender=PostLikes,
    dispatch_uid='post_like_notification'
)
post_save.connect(
    comment_like,
    sender=CommentLikes,
    dispatch_uid='comment_like_notification'
)
post_save.connect(
    comment_notification,
    sender=Comment,
    dispatch_uid='comment_notification'
)
