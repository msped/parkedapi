from django.apps import AppConfig
from .signals import notify

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        from .handler import notify_handler
        notify.connect(notify_handler)
