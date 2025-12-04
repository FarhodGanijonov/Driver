from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
User = get_user_model()

# Driver websocket consumer
class DriverConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        # Header orqali token olish
        token = None
        for header in self.scope['headers']:
            if header[0].decode() == 'authorization':
                auth_value = header[1].decode()  # "Bearer <token>"
                if auth_value.startswith("Bearer "):
                    token = auth_value.split(" ")[1]

        if not token:
            await self.close()
            return

        # Tokenni tekshirish
        try:
            validated_token = JWTAuthentication().get_validated_token(token)
            self.driver = await database_sync_to_async(User.objects.get)(id=validated_token["user_id"])
            print(f"Driver connected: id={self.driver.id}, full_name={self.driver.full_name}")
        except Exception:
            await self.close()
            return

        self.group_name = f"driver_{self.driver.id}"


        # Driver ONLINE qilamiz
        await self.set_driver_online_status(True)

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        if hasattr(self, "driver"):
            await self.set_driver_online_status(False)
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Driver assigned event
    async def driver_assigned(self, event):
        await self.send_json({
            "event": "ORDER_ASSIGNED",
            "order_id": event["order_id"],
            "client_name": event["client_name"],
            "pickup_point": event["pickup_point"],
            "description": event["description"]
        })


    @database_sync_to_async
    def set_driver_online_status(self, online: bool):
        if self.driver:
            self.driver.is_online = online
            # Agar driver busy bo‘lsa offline qilinmaydi
            if self.driver.status != "busy":
                self.driver.status = "online" if online else "offline"
            self.driver.save()


