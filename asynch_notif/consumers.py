import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import os , django
django.setup()
from .models import * 

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender_id = text_data_json["send"]
        receiver_id = text_data_json["recieve"]
        content = text_data_json["message"]
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        Notification = notification.objects.create(sender=sender, reciever=receiver, content=content)

        # Send acknowledgment to sender
        self.send(text_data=json.dumps({"message": "Message sent successfully!"}))

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": content}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket of the receiver
        self.send(text_data=json.dumps({"message": message}))