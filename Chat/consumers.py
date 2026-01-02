
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            from Auth import models
            
            self.room_name = self.scope['url_route']["kwargs"]['room_name']
            self.room_group_name = f"chat_{self.room_name}"
            self.user = self.scope['user']

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

        except:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        try:
            message = data["message"]
            if not message:
                return
            
            await self.saveMessage(message)

        except json.JSONDecodeError:
            return

        try:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chatMessage",
                    "message": message
                }
            )
        except Exception as e:
            print('group send failed: ', e)

    async def chatMessage(self, event):
        try:
            await self.send(text_data=json.dumps({
                "message": event["message"]
            }))
        
        except Exception as e:
            await self.close()
    
    @database_sync_to_async
    def saveMessage(self, message):
        from Auth import models

        print(f"{self.user.first_name} {self.user.last_name} {self.user.username}: {message}")

