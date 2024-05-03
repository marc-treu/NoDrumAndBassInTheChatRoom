import json
import uuid


from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

GAME_GROUP_NAME = "game_group"


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            GAME_GROUP_NAME + "_chat", self.channel_name
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            GAME_GROUP_NAME + "_chat", self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data, **kwargs):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            GAME_GROUP_NAME + "_chat", {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "user": event.get("user")}))


class ShifumiConsumer(WebsocketConsumer):
    game_group_name = "game_group"
    players = {}
    msg = []

    def connect(self):
        self.player_id = str(uuid.uuid4())
        self.accept()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            GAME_GROUP_NAME + "_game", self.channel_name
        )

        # self.send(
        #     text_data=json.dumps({"type": "playerId", "playerId": self.player_id})
        # )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            GAME_GROUP_NAME + "_game", self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data, **kwargs):
        text_data_json = json.loads(text_data)
        play = text_data_json["play"]
        async_to_sync(self.channel_layer.group_send)(
            GAME_GROUP_NAME + "_game", {"type": "chat.message", "message": f"{self.player_id} has play {play}", "user": text_data_json["user"]}
        )

    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": event.get("message"), "user": event.get("user")}))
