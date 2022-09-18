from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification

class MarkAsRead(APIView):
    def get(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            id=notification_id
        )
        notification.mark_as_read()
        return Response(status=status.HTTP_200_OK)

class MarkAsUnread(APIView):
    def get(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            id=notification_id
        )
        notification.mark_as_unread()
        return Response(status=status.HTTP_200_OK)
