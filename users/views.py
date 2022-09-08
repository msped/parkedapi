from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import Profile
from .serializers import ChangePasswordSerializer

class BlacklistTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Profile
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        current_user = request.user
        profile = Profile.objects.get(id=current_user.id)
        if serializer.is_valid():
            if not profile.check_password(serializer.data.get("old_password")):
                return Response(
                    {"error": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            profile.set_password(serializer.data.get("new_password"))
            profile.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, username):
        obj = get_object_or_404(Profile, username=username)
        return obj

    def post(self, request, username):
        url_username = self.get_object(username)
        current_user = self.get_object(request.user.username)
        if current_user.following.filter(username=url_username.username).exists():
            current_user.following.remove(url_username)
            return Response(status=status.HTTP_204_NO_CONTENT)
        current_user.following.add(url_username)
        return Response(status=status.HTTP_201_CREATED)
