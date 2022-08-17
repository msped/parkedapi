from rest_framework import serializers
from .models import Post, PostLikes, Comment, CommentLikes

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'author',
            'image',
            'created_at',
            'description',
            'comments_enabled',
        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'profile',
            'post',
            'created_at'
        ]

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikes
        fields = [
            'post'
            'profile'
        ]
