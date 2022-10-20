from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, CommentLikes, Post, PostLikes
from .serializers import (
    CommentSerializer,
    PostSerializer,
    PostLikeSerializer,
    CommentsLikeSerializer,
    PostPatchSerializer,
)

# Create your views here.

class PostNew(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

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

class PostGetUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return PostPatchSerializer
        return PostSerializer

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
            author_id=self.request.user.id,
            post=self.get_object()
        )

class CommentLike(APIView):
    serializer_class = CommentsLikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        # Create a post like obj or delete it
        comment = Comment.objects.get(id=comment_id)
        obj, created = CommentLikes.objects.get_or_create(
            comment=comment,
            profile_id=request.user.id
        )
        if created:
            return Response(status=status.HTTP_201_CREATED)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentGetUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'comment_id'
    queryset = Comment.objects.all()
