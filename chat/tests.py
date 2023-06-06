from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from chat.models import Room, RoomJoin
from users.models import User
from django.urls import reverse


class Test(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "testuser@test.com", "password": "1234"}
        cls.user = User.objects.create_user("testuser@test.com", "1234")

    def test_case_rooms(self):
        user = User.objects.create(email="test@test.com", password="test")
        access_token = self.client.post(reverse("login"), self.user_data).data["token"][
            "access"
        ]
        url = reverse("room_view")
        token = f"Bearer {access_token}"
        print(url)
        client = APIClient()
        a = client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        data = {"user": user.id}
        temp = self.client.post(path=url, data=data, headers={"Authorization": token})

        result = self.client.get(path=url, headers={"Authorization": token})
