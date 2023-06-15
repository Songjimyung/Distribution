from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from users.models import User
from campaigns.models import Campaign
from .models import Payment, RegisterPayment
from faker import Faker
from config import settings
import tempfile, json
from PIL import Image

def arbitrary_image(temp_text):
    """
    작성자 : 최준영
    내용 : 테스트용 임의 이미지 생성 함수입니다.
    최초 작성일 : 2023.06.08
    업데이트 일자 :
    """
    size = (50, 50)
    image = Image.new("RGBA", size)
    image.save(temp_text, "png")
    return temp_text

class PaymentTest(APITestCase):
    '''
    작성자: 송지명
    내용: 결제 카드 등록 및 예약결제 테스트 코드
    작성일: 2023.06.12
    업데이트날짜 : 2023.06.14
    '''

    @classmethod
    def setUpTestData(cls):
        cls.username = User.objects.create_user(email="testuser@test.com", username="test", password="test")
        cls.user_data = {"email": "testuser@test.com", "password": "test"}
        cls.faker = Faker()
        cls.payment_data = {
            "card_number": settings.CARD_NUMBER,
            "expiry_at": settings.EXPIRY_AT,
            "birth": settings.BIRTH,
            "pwd_2digit": settings.PWD_2DIGIT
        }
            
        cls.campaign_data = {
            "title": "탄소발자국 캠페인 모집",
            "content": "더 나은 세상을 위한 지구별 눈물 닦아주기, 이제 우리가 행동에 나설 때입니다.",
            "members": "200",
            "current_members": "0",
            "campaign_start_date": "2023-06-09",
            "campaign_end_date": "2023-06-16",
            "activity_start_date": "2023-06-17",
            "activity_end_date": "2023-06-27",
            "image": "",
            "is_funding": "True",
            "status": "1",
        }
        temp_img = tempfile.NamedTemporaryFile()
        temp_img.name = "image.png"
        image_file = arbitrary_image(temp_img)
        image_file.seek(0)
        cls.campaign_data["image"] = image_file.name
        cls.campaign_data['user'] = User.objects.get(id=1)
        cls.campaign = Campaign.objects.create(**cls.campaign_data)
        cls.campaign_id = cls.campaign.id
           
    def setUp(self):
        self.access_token = self.client.post(reverse('log_in'), self.user_data).data['access']
        self.client = APIClient()
    def test_register_payment(self):
        '''
        결제정보 등록 테스트 코드
        '''
        response = self.client.post(
            path=reverse("register_payment"),
            data=self.payment_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(response.status_code, 200)

    def test_register_payment_view(self):
        '''
        결제정보 조회 테스트코드
        '''
        response = self.client.get(
            path=reverse("register_payment"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(response.status_code, 200)
    def test_create_payment_schedule(self):
        '''
        결제정보 등록 후 예약결제 테스트 코드
        '''
        card_data = self.client.post(
            path=reverse("register_payment"),
            data=self.payment_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        selected_card_data = card_data.data['card_number']
        selected_data = RegisterPayment.objects.get(card_number=selected_card_data)
        selected_data_id = selected_data.id
        schedule_data = {
            "campaign": self.campaign.id,  
            "amount": '1000',
            "selected_card": selected_data_id
        }
        response = self.client.post(
            path=reverse("schedule_payment"),
            data=schedule_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(response.status_code, 200)
    
    def test_view_payment_schedule(self):
        '''
        예약결제 확인 테스트 코드
        '''
        response = self.client.get(reverse('schedule_payment'))
        self.assertEqual(response.status_code, 200)