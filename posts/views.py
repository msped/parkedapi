from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, CommentLikes, Post, PostLikes
from .serializers import CommentSerializer, PostSerializer, PostLikeSerializer

# Create your views here.

class PostNew(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

class CommentNew(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

class PostLike(APIView):
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        # Create a post like obj or delete it
        obj, created = PostLikes.objects.get_or_create(
            post__slug=slug,
            profile__id=request.user.id
        )
        if created:
            return Response(status=status.HTTP_201_CREATED)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
