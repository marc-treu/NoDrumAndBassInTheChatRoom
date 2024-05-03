import json
import uuid


from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer


class ShifumiConsumer(WebsocketConsumer):
    game_group_name = "game_group"
    players = {}
    msg = []

    def connect(self):
        self.player_id = str(uuid.uuid4())
        self.accept()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name, self.channel_name
        )

        # self.send(
        #     text_data=json.dumps({"type": "playerId", "playerId": self.player_id})
        # )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data, **kwargs):
        text_data_json = json.loads(text_data)
        action = text_data_json.get("action")
        if action == "send_message":
            self.handle_message(text_data_json)
        elif action == "play":
            self.handle_play(text_data_json)

    def handle_message(self, json):
        message = json["message"]
        print(self.player_id, " envoie le msg suivant:", message)

        # Store the message in cache
        self.msg.append({"message": message, "username": self.player_id})

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {"type": "chat.message", "message": message}
        )

    def handle_play(self, json):
        play = json["play"]
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {"type": "chat.message", "message": f"{self.player_id} has play {play}", "user": json["user"]}
        )

    # Receive message from room group
    def chat_message(self, event):

        message = event["message"]
        print(self.player_id, " Recoie le msg suivant:", message)

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "user": event.get("user")}))
