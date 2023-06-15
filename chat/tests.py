from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from chat.models import Room, Message
from users.models import User
from django.urls import reverse


class Test(APITestCase):
    @classmethod
    def setUp(self):
        self.counselor = User.objects.create_superuser(email="counselor@test.com",
                                                       username='counselor', password='password')
        self.advisee = User.objects.create_user(email="advisee@test.com",
                                                username='advisee', password='password')
        self.room = Room.objects.create(
            counselor=self.counselor, advisee=self.advisee)

    def test_send_message(self):
        # 메시지 전송 테스트
        message = Message.objects.create(
            room_id=self.room, user_id=self.counselor, message='Hello')
        self.assertEqual(message.room_id, self.room)
        self.assertEqual(message.user_id, self.counselor)
        self.assertEqual(message.message, 'Hello')

    def test_update_read_status(self):
        # 메시지 읽음 상태 업데이트 테스트
        message = Message.objects.create(
            room_id=self.room, user_id=self.counselor, message='Hello')
        self.assertFalse(self.room.counselor_read)
        self.assertFalse(self.room.advisee_read)

        # 상담자가 메시지를 읽음 처리
        self.room.counselor_read = True
        self.room.save()
        self.assertTrue(self.room.counselor_read)
        self.assertFalse(self.room.advisee_read)

        # 피상담자가 메시지를 읽음 처리
        self.room.advisee_read = True
        self.room.save()
        self.assertTrue(self.room.counselor_read)
        self.assertTrue(self.room.advisee_read)
