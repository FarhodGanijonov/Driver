import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

# Client websocket consumer
class ClientOrderConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        # Tokenni headerdan olish
        token = None
        for header in self.scope['headers']:
            if header[0].decode() == 'authorization':
                auth_value = header[1].decode()
                if auth_value.startswith("Bearer "):
                    token = auth_value.split(" ")[1]

        if not token:
            await self.close()
            return

        # Tokenni tekshirish va clientni olish
        try:
            validated_token = JWTAuthentication().get_validated_token(token)
            self.client = await database_sync_to_async(User.objects.get)(id=validated_token["user_id"])
            print(f"Client connected: id={self.client.id}, full_name={self.client.full_name}")
        except Exception:
            await self.close()
            return

        # Client ONLINE qilamiz
        await self.set_client_online_status(True)

        self.group_name = f"client_{self.client.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "client"):
            # Clientni offline qilish
            await self.set_client_online_status(False)
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # ORDER_ASSIGNED event
    async def order_assigned(self, event):
        await self.send(text_data=json.dumps({
            "message_type": "ORDER_ASSIGNED",
            "order_id": event["order_id"],
            "driver_id": event["driver_id"],
            "driver_name": event["driver_name"]
        }))


    # Client status online yoki offline qilish
    @database_sync_to_async
    def set_client_online_status(self, online: bool):
        self.client.is_online = online
        self.client.status = "active" if online else "inactive"
        self.client.save()
