from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .tasks import ai_respond_task
import json
import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    chat_history = ""
    ai_is_active = [False]

    async def connect(self):
        try:
            self.user = self.scope['user']

            await self.loadImage()

            if not self.user.is_authenticated:
                await self.close(code=4001)
                return
            
            self.room_name = self.scope['url_route']["kwargs"]['room_name']
            self.room_group_name = f"chat_{self.room_name}"

            await self.getChatHistory()

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
            if '@modulo' in message:
                # Sending user details first
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chatMessage",
                        "message": message,
                        'username': f"{self.user.first_name}",
                        'image_url': self.image_url,
                        "timestamp": datetime.datetime.now().isoformat(),
                        "ai_typing": False,
                    }
                )
                # Sending AI loading message
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chatMessage",
                        "message": "typing...",
                        "username": "moduloAI",
                        "image_url": None,
                        "timestamp": datetime.datetime.now().isoformat(),
                        "ai_typing": True,
                    }
                )

                # 3️⃣ Send task to background worker
                self.ai_is_active = True
             
                ai_respond_task.delay(
                    prompt=message,
                    room_group_name=self.room_group_name,
                    chat_history=self.chat_history,
                    ai_is_active=self.ai_is_active
                )


                # save chat history for ai response generation
                #self.chat_history += f"chat: {message}\n"

            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chatMessage",
                        "message": message,
                        'username': f"{self.user.first_name}",
                        'image_url': self.image_url,
                        "timestamp": datetime.datetime.now().isoformat(),
                        "ai_typing": False,
                    }
                )
        except Exception as e:
            print('group send failed: ', e)

    async def chatMessage(self, event):
        try:
            # check if the message is from AI or user
            if event['username'] == 'moduloAI' and not event['ai_typing']:
                self.chat_history += f"AI: {event['message']}\n"
                self.ai_is_active = False
                await self.saveAIresponse(event['message'])
            else:
                self.chat_history += f"{event['username']}: {event['message']}\n"

            await self.send(text_data=json.dumps({
                "message": event["message"],
                'username': event["username"],
                'image_url': event['image_url'],
                "timestamp": event["timestamp"],
                'ai_typing': event["ai_typing"],
            }))
        
        except Exception as e:
            await self.close()
    
    def generateAIresponse(self, new_message):
        from AI_model import views
        response = views.aiGroupChat(self.chat_history, new_message)
        return response
    
    @database_sync_to_async
    def saveMessage(self, text):
        try:
            from Auth import models

            group = models.Group.objects.get(slug=self.room_name)
            if not models.GroupMessages.objects.filter(group=group).exists():
                message = models.GroupMessages(group=group)
                message.save()

            message = models.GroupMessages.objects.get(group=group)

            data = {
                'user_first_name': self.user.first_name,
                'username':self.user.username,
                'message': text,
                'image_url': self.image_url,
                'timestamp': f'{datetime.datetime.now().isoformat()}',
                'ai': False
            }
            message.messages.append(data)
            message.msg_index += 1
            message.save()
            return
        
        except Exception as e:
            print("failed to save message", e)
            return

    @database_sync_to_async
    def saveAIresponse(self, text):
        try:
            from Auth import models

            group = models.Group.objects.get(slug=self.room_name)
            if not models.GroupMessages.objects.filter(group=group).exists():
                message = models.GroupMessages(group=group)
                message.save()

            message = models.GroupMessages.objects.get(group=group)

            data = {
                'user_first_name': 'moduloAI',
                'username': 'moduloAI',
                'message': text,
                'timestamp': f'{datetime.datetime.now().isoformat()}',
                'ai': True
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
        
    @database_sync_to_async
    def getChatHistory(self):
        try:
            from Auth import models

            group = models.Group.objects.get(slug=self.room_name)
            if models.GroupMessages.objects.filter(group=group).exists():
                messages = models.GroupMessages.objects.get(group=group)
                self.temporarySaveChatHistory(messages.messages)
                return
            else:
                return []
        
        except Exception as e:
            print("failed to get chat history", e)
            return []

    def temporarySaveChatHistory(self, messages, user):
        for message in messages:
            self.chat_history += f"{message['username']}: {message['message']}\n"
