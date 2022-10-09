from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.utils import timezone
from swapper import load_model

from .serializers import NotificationSerializer

def notify_handler(sender, **kwargs):
    # Pull the options out of kwargs
    kwargs.pop('signal', None)
    profile = kwargs.pop('profile')
    recipient = kwargs.pop('recipient')
    optional_objs = [
        (kwargs.pop(opt, None), opt)
        for opt in ('target',)
    ]
    read = kwargs.pop('read', False)
    text = kwargs.pop('text')
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
            sender=profile,
            recipient=recipient,
            read=read,
            timestamp=timestamp,
            text=text
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

    return new_notifications
