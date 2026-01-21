from django.urls import path
from . import views


urlpatterns = [
    path('', views.groupHomeRender, name='group_home'),
    path('chat-room/<str:group>/', views.chatRoomRender, name='chat_room'),
    path('group-detail/<str:group>/', views.groupDetailRender, name='group_detail')
]