import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ClientOrderConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.client_id = self.scope["url_route"]["kwargs"]["client_id"]
        self.group_name = f"client_{self.client_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # WebSocket event handler
    async def order_assigned(self, event):
        await self.send(text_data=json.dumps({
            "message_type": "ORDER_ASSIGNED",
            "order_id": event["order_id"],
            "driver_id": event["driver_id"],
            "driver_name": event["driver_name"]
        }))
