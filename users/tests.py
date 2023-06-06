from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class SignUpTest(APITestCase):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.07
    작성내용 : 회원가입시 발생할 수 있는 이슈들에 관한 테스트 코드
    업데이트 날짜 : 
    '''
    def test_signup(self):
        url = reverse("sign_up")
        user_data = {
            "email": "user1@google.com",
            "name": "user1",
            "password": "Test!!11",
            "re_password": "Test!!11",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)
    
    def test_signup_wrong_password_validate(self):
        url = reverse("sign_up")
        user_data = {
            "email": "user1@google.com",
            "name": "user1",
            "password": "test11",
            "re_password": "test11",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
    
    def test_signup_wrong_password_pattern(self):
        url = reverse("sign_up")
        user_data = {
            "email": "user1@google.com",
            "name": "user1",
            "password": "tttTTT111!!!",
            "re_password": "tttTTT111!!!",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
    
    def test_signup_not_re_password(self):
        url = reverse("sign_up")
        user_data = {
            "email": "user1@google.com",
            "name": "user1",
            "password": "Test!!11",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)


class LoginTest(APITestCase):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.07
    작성내용 : 로그인시 발생할 수 있는 이슈들에 관한 테스트 코드
    업데이트 날짜 : 
    '''
    def setUp(self):
        self.url = reverse('log_in')
        self.user_data = User.objects.create_user(email="user1@google.com", name="test", password="Test!!11")
    
    def test_login(self):
        user ={
            "email": "user1@google.com",
            "password":"Test!!11",
        }
        response = self.client.post(self.url, user, format='json')
        self.assertEqual(response.status_code, 200)

    def test_login_wrong_password(self):
        user ={
            "email": "user1@google.com",
            "password":"test!!11",
        }
        response = self.client.post(self.url, user, format='json')
        self.assertEqual(response.status_code, 401)