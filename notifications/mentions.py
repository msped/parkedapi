import re

from posts.models import Comment, Post
from users.models import Profile

from .signals import notify

def check_instance(target):
    if isinstance(target, Comment):
        username = target.post.author.username
    elif isinstance(target, Post):
        username = target.author.username
    else:
        raise Exception("Unexpected type of target.")
    return username

def check_for_mention(profile, target, content, text):
    mentions = re.findall(r'\B@([._a-z0-9]{4,30})\b', content)
    instance = check_instance(target)
    if instance in mentions:
        mentions.remove(instance)
    if mentions:
        mention_instances = Profile.objects.filter(
            username__in=mentions
        )
        notify.send(
            sender=None,
            profile=profile,
            recipient=mention_instances,
            target=target,
            text=text
        )
