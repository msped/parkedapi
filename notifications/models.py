from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from users.models import Profile

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
