import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'cart_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'cart_update')

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': message_type,
                'data': data
            }
        )

    # Receive message from room group
    async def cart_update(self, event):
        # Send to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'cart_update',
            'data': event['data']
        }))

    async def cart_item_added(self, event):
        await self.send(text_data=json.dumps({
            'type': 'cart_item_added',
            'data': event['data']
        }))

    async def cart_item_removed(self, event):
        await self.send(text_data=json.dumps({
            'type': 'cart_item_removed',
            'data': event['data']
        }))
