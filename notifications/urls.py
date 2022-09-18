from django.urls import path

from .views import MarkAsRead, MarkAsUnread

urlpatterns = [
    path('read/<int:notification_id>/', MarkAsRead.as_view(), name="mark_as_read"),
    path(
        'unread/<int:notification_id>/',
        MarkAsUnread.as_view(),
        name="mark_as_unread"
    ),
]
