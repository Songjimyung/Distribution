from django.urls import path
from chat import views

urlpatterns = [
    path("room/", views.RoomView.as_view(), name="room_view"),
    path("roominfo/", views.ChatRoom.as_view(), name="room_info"),
]
