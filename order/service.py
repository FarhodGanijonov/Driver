from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from users.models import AbstractUser


async def assign_driver(order):
    """
        Berilgan orderga mavjud bo‘lgan online driverni biriktiradi va
        driver ham, client ham WebSocket orqali real vaqt xabari oladi.
        Agar hech qanday driver topilmasa, clientga xabar yuboriladi.

    """
    driver = await AbstractUser.objects.filter(
        role="driver",
        is_online=True,
        status="online"
    ).afirst()  # async ORM

    channel_layer = get_channel_layer()

    if driver:
        # Driver biriktiriladi
        order.driver = driver
        order.status = "ASSIGNED"
        await database_sync_to_async(order.save)()

        # Driver band qilinadi
        driver.status = "busy"
        driver.current_order = order
        await database_sync_to_async(driver.save)()

        # Driverga realtime xabar
        await channel_layer.group_send(
            f"driver_{driver.id}",
            {
                "type": "order_assigned",
                "order_id": order.id,
                "client_id": order.client.id,
                "client_name": order.client.full_name,
                "pickup_point": {
                    "lat": order.location.y,
                    "lon": order.location.x
                },
                "description": order.description
            }
        )

        # Clientga realtime xabar
        await channel_layer.group_send(
            f"client_{order.client.id}",
            {
                "type": "order_assigned",
                "order_id": order.id,
                "driver_id": driver.id,
                "driver_name": driver.full_name,
                "driver_status": driver.status,
                "driver_location": {
                    "lat": driver.point.y,
                    "lon": driver.point.x
                }
            }
        )

        return driver
    else:
        # Hech qanday driver topilmadi, clientga xabar
        await channel_layer.group_send(
            f"client_{order.client.id}",
            {
                "type": "order.no_driver",
                "message": "No available driver at the moment."
            }
        )
        return None


