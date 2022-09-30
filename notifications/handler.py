from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.utils import timezone
from swapper import load_model

from .serializers import NotificationSerializer
from .signals import notify

def notify_handler(**kwargs):
    # Pull the options out of kwargs
    kwargs.pop('signal', None)
    sender = kwargs.pop('sender')
    recipient = kwargs.pop('recipient')
    optional_objs = [
        (kwargs.pop(opt, None), opt)
        for opt in ('target',)
    ]
    read = kwargs.pop('read', False)
    timestamp = kwargs.pop('timestamp', timezone.now())
    notification_model = load_model('notifications', 'Notification')

    # Check if User or Group
    if isinstance(recipient, Group):
        recipients = recipient.user_set.all()
    elif isinstance(recipient, (QuerySet, list)):
        recipients = recipient
    else:
        recipients = [recipient]

    new_notifications = []

    for recipient in recipients:
        newnotify = notification_model(
            sender=sender,
            recipient=recipient,
            read=read,
            timestamp=timestamp
        )

        # Set optional objects
        for obj, opt in optional_objs:
            if obj is not None:
                setattr(newnotify, f'{opt}_object_id', obj.pk)
                setattr(newnotify, f'{opt}_content_type',
                        ContentType.objects.get_for_model(obj))

        newnotify.save()
        serializer = NotificationSerializer(newnotify)
        new_notifications.append(serializer.data)

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f'notifications-{sender.id}',
            {
                'type': 'notification',
                'message': serializer.data
            }
        )

    return new_notifications


# connect the signal
notify.connect(notify_handler, dispatch_uid='notifications.models.notification')
