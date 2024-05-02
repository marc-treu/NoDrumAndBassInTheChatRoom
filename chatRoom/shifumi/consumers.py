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

        self.send(
            text_data=json.dumps({"type": "playerId", "playerId": self.player_id})
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        print(self.player_id, " envoie le msg suivant:", message)

        # Store the message in cache
        self.msg.append({"message": message, "username": self.player_id})

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):

        message = event["message"]
        print(self.player_id, " Recoie le msg suivant:", message)

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
