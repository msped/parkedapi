from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, CommentLikes, Post, PostLikes
from .serializers import (
    CommentSerializer,
    PostSerializer,
    PostLikeSerializer,
    CommentsLikeSerializer
)

# Create your views here.

class PostNew(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

class CommentNew(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'slug'

    def get_object(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        post = Post.objects.get(slug=slug)
        return post

    def perform_create(self, serializer):
        serializer.save(
            profile_id=self.request.user.id,
            post=self.get_object()
        )

class PostLike(APIView):
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        # Create a post like obj or delete it
        post = Post.objects.get(slug=slug)
        obj, created = PostLikes.objects.get_or_create(
            post=post,
            profile_id=request.user.id
        )
        if created:
            return Response(status=status.HTTP_201_CREATED)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentLike(APIView):
    serializer_class = CommentsLikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        # Create a post like obj or delete it
        comment = Post.objects.get(slug=slug)
        obj, created = CommentLikes.objects.get_or_create(
            comment=comment,
            profile_id=request.user.id
        )
        if created:
            return Response(status=status.HTTP_201_CREATED)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
