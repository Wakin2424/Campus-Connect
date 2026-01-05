from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user = self.scope['user']

            await self.loadImage()

            if not self.user.is_authenticated:
                await self.close(code=4001)
                return
            
            self.room_name = self.scope['url_route']["kwargs"]['room_name']
            self.room_group_name = f"chat_{self.room_name}"

            is_member = await self.user_GroupValidation(self.room_name, self.user)

            if not is_member:
                await self.close(code=4003)
                return
            
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
                    "message": message,
                    'username': f"{self.user.first_name}",
                    'image_url': self.image_url,
                    "timestamp": datetime.datetime.now().isoformat(),
                }
            )
        except Exception as e:
            print('group send failed: ', e)

    async def chatMessage(self, event):
        try:
            await self.send(text_data=json.dumps({
                "message": event["message"],
                'username': event["username"],
                'image_url': event['image_url'],
                "timestamp": event["timestamp"],
            }))
        
        except Exception as e:
            await self.close()
    
    @database_sync_to_async
    def saveMessage(self, text):
        try:
            from Auth import models

            group = models.Group.objects.get(slug=self.room_name)
            if not models.GroupMessages.objects.filter(group=group).exists():
                message = models.GroupMessages(group=group)
                message.save()

            print('message exists')

            message = models.GroupMessages.objects.get(group=group)

            data = {
                'user_first_name': self.user.first_name,
                'username':self.user.username,
                'message': text,
                'image_url': self.image_url,
                'timestamp': f'{datetime.datetime.now().isoformat()}'
            }
            message.messages.append(data)
            message.msg_index += 1
            message.save()
            return
        
        except Exception as e:
            print("failed to save message", e)
            return

    
    @database_sync_to_async
    def user_GroupValidation(self, group, user):
        try:
            from Auth import models

            user = models.AuthCustomuser.objects.get(id=user.id)
            group = models.Group.objects.get(slug=group)
            
            if models.GroupMember.objects.filter(group=group, user=user).exists():
                return True
            else:
                return False
        
        except:
            return False

    @database_sync_to_async
    def loadImage(self):
        try:
            from Auth import models
            user = models.AuthCustomuser.objects.get(id=self.user.id)
            self.image_url = f'{user.image.file.url}' if user.image != None else None
            return
        
        except:
            self.image_url = None
            return 

