from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from chat.models import Room, RoomJoin
from users.models import User
from django.urls import reverse


class Test(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_data = {"email": "admin@admin.com",
                          "username": "admin", "password": "Aedeye12up!"}
        cls.admin = User.objects.create_superuser(
            email="admin@admin.com", username="admin", password="Aedeye12up!")

    def test_case_create_rooms(self):
        email = "test@test.com"
        user = self.client.post(reverse("sign_up"), {
                                "email": email, "username": "test1", "password": "Radeye12ui!", "re_password": "Radeye12ui!"})
        access_token = self.client.post(reverse(
            "log_in"), {"email": "test@test.com", "password": "Radeye12ui!"}).data['access']

        url = reverse("room_view")
        token = f"Bearer {access_token}"
        client = APIClient()

        a = client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        temp = self.client.post(path=url, headers={"Authorization": token})
        result = self.client.get(path=url, headers={"Authorization": token})
        user_list = result.data.get(1)
        self.assertIn(email, user_list)
