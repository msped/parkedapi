from rest_framework import serializers
from posts.models import Comment, CommentLikes, PostLikes, Post
from posts.serializers import (CommentSerializer, CommentsLikeSerializer,
                               PostLikeSerializer, PostSerializer)
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
        elif isinstance(value, Post):
            serializer = PostSerializer(value)
        else:
            raise Exception("Unexpected type of target object.")

        return serializer.data

class NotificationSerializer(serializers.ModelSerializer):
    sender = ShortProfileSerializer()
    recipient = ShortProfileSerializer()
    target = TargetObjectSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'sender',
            'recipient',
            'target',
            'read',
            'timestamp',
            'text'
        ]
