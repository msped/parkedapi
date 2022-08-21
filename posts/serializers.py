from rest_framework import serializers
from .models import Post, PostLikes, Comment, CommentLikes

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = [
            'author',
            'image',
            'description',
            'comments_enabled',
        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'profile',
            'post'
        ]

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikes
        fields = [
            'post'
            'profile'
        ]

class CommentsLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLikes
        fields = [
            'comment'
            'profile'
        ]
