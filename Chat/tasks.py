from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import datetime
from AI_model import views


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def ai_respond_task(self, prompt, room_group_name, ai_is_active, chat_history=''):
    """
    Runs AI in background and sends response to WebSocket group
    """
    print('starting AI process')

    ai_is_active = False
    # 🔥 Simulate AI call
    ai_response = views.aiGroupChat(chat_history, prompt)
    if ai_response == None:
        ai_response = "Sorry, I couldn't generate a response. Please try again."
    print(ai_response)

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            "type": "chatMessage",
            "message": ai_response,
            "username": "moduloAI",
            "image_url": None,
            "timestamp": datetime.datetime.now().isoformat(),
            "ai_typing": False,
            'email': '',
        }
    )


