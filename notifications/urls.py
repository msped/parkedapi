from django.urls import path

from .views import (GetAll, GetNotification, MarkAllAsRead, MarkAsRead,
                    MarkAsUnread)

urlpatterns = [
    path('read/<int:notification_id>/', MarkAsRead.as_view(), name="mark_as_read"),
    path(
        'unread/<int:notification_id>/',
        MarkAsUnread.as_view(),
        name="mark_as_unread"
    ),
    path('read/all/', MarkAllAsRead.as_view(), name="mark_all_as_read"),
    path('all/', GetAll.as_view(), name="get_all_notifications"),
    path('<int:pk>/', GetNotification.as_view(), name="get_notification"),
]
