from users.models import User
from django.db import models


class Room(models.Model):
    """
    작성자 : 박지홍
    내용 : 채팅을 위한 방을 만드는 모델
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.15
    #06.15 : 
        - 채팅방을 읽었는지 유무를 판단하기 위한 필드를 추가.
        - 1:1 통신만 존재함으로 인해 기존의 구조를 한 단계 덜어냄.
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    counselor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="counselor_user", db_column="counselor")
    advisee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="advisee_user", db_column="advisee")
    counselor_read = models.BooleanField(default=False)
    advisee_read = models.BooleanField(default=False)

    class Meta:
        db_table = "room"


class Message(models.Model):
    """
    작성자 : 박지홍
    내용 : 채팅방에 유저가 남기는 메세지를 보관할 모델
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.15
    #06.15 : 1:1 통신만 존재함으로 인해 기존의 구조를 한 단계 덜어냄.
    """

    user_id = models.ForeignKey(
        User, related_name="messages", on_delete=models.CASCADE, db_column="user_id"
    )
    room_id = models.ForeignKey(
        Room, related_name="messages", on_delete=models.CASCADE, db_column="room_id"
    )
    message = models.CharField(max_length=512)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"

    def __str__(self):
        return self.user_id.email
