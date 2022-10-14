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

class PostPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'description',
            'comments_enabled',
        ]

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.ReadOnlyField()
    class Meta:
        model = Comment
        fields = [
            'author',
            'post',
            'content',
            'created_at'
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
