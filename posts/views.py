from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Comment, CommentLikes, Post, PostLikes
from .serializers import CommentSerializer, PostSerializer

# Create your views here.

class PostNew(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

class CommentNew(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
