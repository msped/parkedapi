from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from swapper import load_model
from users.models import Profile

from .signals import notify

# Create your models here.

class NotificationQuerySet(models.query.QuerySet):
    def unread(self):
        return self.filter(read=False)

    def read(self):
        return self.filter(read=True)

    def mark_all_as_read(self, recipient):
        qset = self.unread()
        qset = qset.filter(recipient=recipient)
        return qset.update(read=True)

    def mark_all_as_unread(self, recipient):
        qset = self.read()
        qset = qset.filter(recipient=recipient)
        return qset.update(read=False)

class Notification(models.Model):
    sender = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='sent_from'
    )
    recipient = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='sent_to'
    )
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = NotificationQuerySet.as_manager()

    class Meta:
        ordering = ('-timestamp',)
        index_together = ['recipient', 'read']

    def __str__(self):
        return f'Sent to {self.recipient} - Read: {self.read}'

    def mark_as_read(self):
        if not self.read:
            self.read = True
            self.save()

    def mark_as_unread(self):
        if self.read:
            self.read = False
            self.save()

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
        new_notifications.append(newnotify)

    return new_notifications


# connect the signal
notify.connect(notify_handler, dispatch_uid='notifications.models.notification')
