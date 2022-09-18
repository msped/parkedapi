from rest_framework import serializers
from posts.models import Comment, CommentLikes, PostLikes
from posts.serializers import (CommentSerializer, CommentsLikeSerializer,
                               PostLikeSerializer)
from users.models import Followers
from users.serializers import FollowersSerializer, ShortProfileSerializer

from .models import Notification

class TargetObjectSerializer(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, PostLikes):
            serializer = PostLikeSerializer(value)
        elif isinstance(value, CommentLikes):
            serializer = CommentsLikeSerializer(value)
        elif isinstance(value, Comment):
            serializer = CommentSerializer(value)
        elif isinstance(value, Followers):
            serializer = FollowersSerializer(value)
        else:
            raise Exception("Unexpected type of target object.")

        return serializer.data

class NotificationSerializer(serializers.ModelSerializer):
    sender = ShortProfileSerializer()
    recipient = ShortProfileSerializer()
    target = TargetObjectSerializer()

    class Meta:
        model = Notification
        fields = [
            'sender',
            'recipient',
            'target',
            'read',
            'timestamp'
        ]
