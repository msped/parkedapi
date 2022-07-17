from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
)

class RegisterView(CreateAPIView):
    queryset = Profile.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

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

    def post(self, request, profile_id):
        obj = Profile.objects.get(id=profile_id)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not obj.check_password(serializer.data.get("old_password")):
                return Response(
                    {"error": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            obj.set_password(serializer.data.get("new_password"))
            obj.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
