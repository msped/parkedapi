from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope["user"].is_anonymous:
            self.close()
        else:
            self.group_name = str(self.scope["user"].pk)
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()

    def disconnect(self, code):
        self.close()

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    def notify(self, event):
        self.send(event)
