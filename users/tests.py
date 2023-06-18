from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from users.models import User


class SendEmailTest(APITestCase):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.16
    작성내용 : 회원가입시 이메일 전송 로직에서 발생할 수 있는 경우들을 테스트합니다.
    업데이트 날짜 : 
    '''
    def setUp(self):
        self.url = reverse('send_email')
        
    def test_send_email(self):
        email ={
            'email':'test@test.com'
        }
        response = self.client.post(self.url, email, format='json')
        self.assertEqual(response.status_code,200)
        
    def test_send_email_blank(self):
        email ={
            'email': ""
        }
        response = self.client.post(self.url, email, format ='json')
        self.assertEqual(response.status_code,400)
    
    def test_send_email_already_register_email(self):
        User.objects.create(email="user1@google.com", username="test", password="Test!!11")
        email ={
            'email':'user1@google.com'
        }
        response = self.client.post(self.url, email, format='json')
        self.assertEqual(response.status_code,400)


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
            "check_code": "dXNlcjFAZ29vZ2xlLmNvbQ==",
            "username": "user1",
            "password": "Test!!11",
            "re_password": "Test!!11",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)
    
    def test_signup_wrong_password_validate(self):
        url = reverse("sign_up")
        user_data = {
            "email": "user1@google.com",
            "check_code": "dXNlcjFAZ29vZ2xlLmNvbQ==",
            "username": "user1",
            "password": "test11",
            "re_password": "test11",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
    
    def test_signup_wrong_password_pattern(self):
        url = reverse("sign_up")
        user_data = {
            "email": "user1@google.com",
            "check_code": "dXNlcjFAZ29vZ2xlLmNvbQ==",
            "username": "user1",
            "password": "tttTTT111!!!",
            "re_password": "tttTTT111!!!",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
    
    def test_signup_none_re_password(self):
        url = reverse("sign_up")
        user_data = {
            "email": "user1@google.com",
            "check_code": "dXNlcjFAZ29vZ2xlLmNvbQ==",
            "username": "user1",
            "password": "Test!!11",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)

    def test_signup_none_check_code(self):
        url = reverse("sign_up")
        user_data = {
            "email": "user1@google.com",
            "check_code": "",
            "username": "user1",
            "password": "Test!!11",
            "re_password": ""
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
        self.user_data = User.objects.create_user(email="user1@google.com", username="test", password="Test!!11")
        
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
    
    
class UserListTest(APITestCase):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.16
    작성내용 : 회원정보 조회 시 발생할 수 있는 경우들을 테스트합니다.
    업데이트 날짜 : 
    '''
    def setUp(self):
        self.data = {'email': 'user1@google.com', "password": "Test!!11"}
        self.user = User.objects.create_user(email="user1@google.com", username="test", password="Test!!11")

    def test_get_user_data(self):
        access_token = self.client.post(reverse('log_in'), self.data).data["access"]
        response = self.client.get(
            path=reverse("user_list"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 200)


class UserUpdateWithdrawalTest(APITestCase):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.16
    작성내용 : 회원정보 수정 or 회원 비활성화 시 발생할 수 있는 경우들을 테스트합니다.
    업데이트 날짜 : 
    '''
    def setUp(self):
        self.data = {'email': 'user1@google.com', "password": "Test!!11"}
        self.user = User.objects.create_user('user1@google.com', "dXNlcjFAZ29vZ2xlLmNvbQ==", "Test!!11")

    def test_update_user(self):
        access_token = self.client.post(reverse('log_in'), self.data).data["access"]
        response = self.client.put(
            path=reverse("update_or_withdrawal"),
            data={'email': 'user11@google.com'},
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 200)
    
    def test_withdrawal_user(self):
        access_token = self.client.post(reverse('log_in'), self.data).data["access"]
        response = self.client.delete(
            path=reverse("update_or_withdrawal"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 200)


class PasswordUpdateTest(APITestCase):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.16
    작성내용 : 비밀번호 수정 시 발생할 수 있는 경우들을 테스트합니다.
    업데이트 날짜 : 
    '''
    def test_password_update(self):
        User.objects.create_user(email="user1@google.com", username="test", password="Test!!11")
        access_token = self.client.post(reverse('log_in'), {'email': 'user1@google.com', "password": "Test!!11"}).data["access"]
        response = self.client.put(
            path=reverse("update_password"),
            data={
                "confirm_password": "Test!!11",
                "password": "Test@@22",
                "re_password": "Test@@22"
            },
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 200)


class PasswordResetTest(APITestCase):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.16
    작성내용 : 비밀번호 재설정 시 발생할 수 있는 경우들을 테스트합니다.
    업데이트 날짜 : 
    '''
    def setUp(self):
        self.user = User.objects.create_user("user1@google.com", "test", "Test1234!")
        self.uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        self.token = PasswordResetTokenGenerator().make_token(self.user)
        
    
    def test_password_reset(self):
        response = self.client.put(
            path=reverse("reset_password"),
            data={
                "password": "Test1234!!",
                "re_password": "Test1234!!",
                "uidb64": self.uidb64,
                "token": self.token
            },
        )
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset_blank_fail(self):
        response = self.client.put(
            path=reverse("reset_password"),
            data={
                "password": "",
                "re_password": "Test1234!!",
                "uidb64": self.uidb64,
                "token": self.token
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_password_reset_confirm_blank_fail(self):
        response = self.client.put(
            path=reverse("reset_password"),
            data={
                "password": "Test1234!!",
                "re_password": "",
                "uidb64": self.uidb64,
                "token": self.token
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_password_reset_validation_fail(self):
        response = self.client.put(
            path=reverse("reset_password"),
            data={
                "password": "Test1234",
                "re_password": "Test1234",
                "uidb64": self.uidb64,
                "token": self.token
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_password_reset_validation_same_fail(self):
        response = self.client.put(
            path=reverse("reset_password"),
            data={
                "password": "Test111!",
                "re_password": "Test111!",
                "uidb64": self.uidb64,
                "token": self.token
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_password_reset_same_fail(self):
        response = self.client.put(
            path=reverse("reset_password"),
            data={
                "password": "Test1234!!",
                "re_password": "Test1234!",
                "uidb64": self.uidb64,
                "token": self.token
            },
        )
        self.assertEqual(response.status_code, 400)

    # def test_password_reset_token_fail(self):
    #     response = self.client.put(
    #         path=reverse("reset_password"),
    #         data={
    #             "password": "Test1234!!",
    #             "re_password": "Test1234!!",
    #             "uidb64": self.uidb64,
    #             "token": "1234"
    #         },
    #     )
    #     self.assertEqual(response.status_code, 401)


class PasswordResetEmailTest(APITestCase):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.16
    작성내용 : 비밀번호 찾기(재설정) 인증코드 발급을 위한 이메일 전송 시 발생할 수 있는 경우들을 테스트합니다.
    업데이트 날짜 : 
    '''
    def setUp(self):
        self.user = User.objects.create_user("user1@google.com", "test", "Test1234!")
    
    def test_password_reset_email(self):
        response = self.client.post(
            path=reverse("reset_password_email"), 
            data={"email": "user1@google.com"},
        )
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset_email_fail(self):
        response = self.client.post(
            path=reverse("reset_password_email"), 
            data={"email": "user2@google.com"},
        )
        self.assertEqual(response.status_code, 400)

    def test_password_reset_email_blank_fail(self):
        response = self.client.post(
            path=reverse("reset_password_email"), 
            data={"email": ""},
        )
        self.assertEqual(response.status_code, 400)


class PasswordResetCheckToken(APITestCase):
    '''
    작성자 : 이주한
    작성날짜 : 2023.06.16
    작성내용 : 비밀번호 찾기(재설정) 인증코드가 유효한지 확인 시 발생할 수 있는 경우들을 테스트합니다.
    업데이트 날짜 : 
    '''
    def setUp(self):
        self.user = User.objects.create_user("user1@google.com", "test", "Test1234!")
        self.uidb64 = urlsafe_base64_encode(smart_bytes(self.user.id))
        self.token = PasswordResetTokenGenerator().make_token(self.user)
    
    def test_password_reset_check_token(self):
        response = self.client.get(
            path=reverse("reset_password_token_check",kwargs={"uidb64": self.uidb64, "token": self.token},),
        )
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset_check_token_fail(self):
        response = self.client.get(
            path=reverse("reset_password_token_check", kwargs={"uidb64": "uidb64", "token": "token"})
        )
        self.assertEqual(response.status_code, 401)