from django.urls import path

from .views import MarkAsRead

urlpatterns = [
    path('read/<int:notification_id>/', MarkAsRead.as_view(), name="mark_as_read"),
]