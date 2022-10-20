from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Profile

from .models import Notification
from .serializers import NotificationSerializer

class MarkAsRead(APIView):
    def post(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            id=notification_id
        )
        notification.mark_as_read()
        return Response(status=status.HTTP_200_OK)

class MarkAsUnread(APIView):
    def post(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            id=notification_id
        )
        notification.mark_as_unread()
        return Response(status=status.HTTP_200_OK)

class MarkAllAsRead(APIView):
    def post(self, request):
        profile = get_object_or_404(Profile, id=request.user.id)
        Notification.objects.mark_all_as_read(recipient=profile)
        return Response(status=status.HTTP_200_OK)

class GetAll(ListAPIView):
    serializer_class = NotificationSerializer
    paginate_by = 10

    def get_queryset(self):
        return Notification.objects.filter(recipient__id=self.request.user.id)

class GetNotification(RetrieveAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recipient__id=self.request.user.id)
