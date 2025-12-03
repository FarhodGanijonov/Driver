from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DriverConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.driver_id = self.scope["url_route"]["kwargs"]["driver_id"]
        self.group_name = f"driver_{self.driver_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Driver assigned event
    async def driver_assigned(self, event):
        await self.send_json({
            "event": "ORDER_ASSIGNED",
            "order_id": event["order_id"],
            "client_name": event["client_name"],
            "pickup_point": event["pickup_point"],
            "description": event["description"]
        })




