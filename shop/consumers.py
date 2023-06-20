from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from users.models import User
from .models import ShopProduct


# connect : 사용자와 websocket 연결이 맺어졌을때 호출
# receive : 사용자가 메시지를 보내면 호출 됨
# disconnect : 사용자와 websocket 연결이 끊겼을때 호출
# AsyncWebsocketConsumer 메모 DB 정보 많이 필요 없으면 가능
class RestockConsumer(WebsocketConsumer):
    def connect(self):
        # restock_notifications 그룹에 현재 컨슈머 추가(알림 메세지 수신),
        async_to_sync(self.channel_layer.group_add)(
            "restock_notifications", self.channel_name)
        self.accept()  # 유저 웹 소켓 연결 수락

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "restock_notifications", self.channel_name)

    def receive(self, text_data):
        pass

    def send_notification(self, event):
        # 알림 메시지 클라이언트에게 전송
        message = event['message']
        self.send(text_data=message)
