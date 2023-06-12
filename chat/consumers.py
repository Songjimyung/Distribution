import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Room, Message
from users.models import User


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        """
        작성자 : 박지홍
        내용 : 웹 소켓을 통해 메시지를 조회하고 메시지를 클라이언트로 전송하는 함수.
        최초 작성일 : 2023.06.06
        업데이트 일자 :
        """
        room_id = int(self.room_name)
        messages = Message.last_30_messages(self, room_id=room_id)
        content = {"command": "messages", "messages": self.messages_to_json(messages)}
        self.send_message(content)

    def new_message(self, data):
        """
        작성자 : 박지홍
        내용 : 웹 소켓을 통해 새로운 메시지를 처리하고 메시지를 클라이언트로 전송하는 함수.
        최초 작성일 : 2023.06.06
        업데이트 일자 :
        """
        user_id = data["user_id"]
        room_id = int(self.room_name)

        user_contact = User.objects.filter(id=user_id)[0]
        room_contact = Room.objects.filter(id=room_id)[0]
        message_creat = Message.objects.create(
            user_id=user_contact, room_id=room_contact, message=data["message"]
        )
        content = {
            "command": "new_message",
            "message": self.message_to_json(message_creat),
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            "author": message.user_id.email,
            "content": message.message,
            "timestamp": str(message.created_at),
        }

    commands = {"fetch_messages": fetch_messages, "new_message": new_message}

    def connect(self):
        """
        작성자 : 박지홍
        내용 : 웹 소켓이 연결을 처리하는 함수.
        최초 작성일 : 2023.06.06
        업데이트 일자 :
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        """
        작성자 : 박지홍
        내용 : 웹 소켓이 연결이 종료될 때 호출되는 함수.
        최초 작성일 : 2023.06.06
        업데이트 일자 :
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        """
        작성자 : 박지홍
        내용 : 웹 소켓으로 부터 메시지를 수신할 때 호출되는 함수.
        최초 작성일 : 2023.06.06
        업데이트 일자 :
        """
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        """
        작성자 : 박지홍
        내용 : 채팅 메시지를 웹 소켓으로 전송하는 함수. 
            - 하단의 send_message, chat_message 도 동일 기능 수행.
        최초 작성일 : 2023.06.06
        업데이트 일자 :
        """
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))
