from users.models import User
from django.db import models


class Room(models.Model):
    """
    작성자 : 박지홍
    내용 : 채팅을 위한 방을 만드는 모델
    최초 작성일 : 2023.06.06
    업데이트 일자 :
    """

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "room"


class RoomJoin(models.Model):
    """
    작성자 : 박지홍
    내용 : 채팅방 속에 존재할 유저를 만드는 모델
    최초 작성일 : 2023.06.06
    업데이트 일자 :
    """

    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="roomJoin", db_column="user_id"
    )
    room_id = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="roomJoin", db_column="room_id"
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "roomJoin"


class Message(models.Model):
    """
    작성자 : 박지홍
    내용 : 채팅방에 유저가 남기는 메세지를 보관할 모델
    최초 작성일 : 2023.06.06
    업데이트 일자 :
    """

    user_id = models.ForeignKey(
        User, related_name="message", on_delete=models.CASCADE, db_column="user_id"
    )
    room_id = models.ForeignKey(
        Room, related_name="message", on_delete=models.CASCADE, db_column="room_id"
    )
    message = models.CharField(max_length=512)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "message"

    def __str__(self):
        return self.user_id.email

    def last_30_messages(self, room_id):
        return Message.objects.filter(room_id=room_id).order_by("created_at")[:30]
