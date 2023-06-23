from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User
from .models import ShopProduct, ShopCategory
from faker import Faker
from datetime import timedelta
from django.utils import timezone
import random
from PIL import Image
from io import BytesIO


def arbitrary_image():
    '''
    작성자:장소은
    내용: arbitrary_image()함수와 BytesIO를 사용하여 50x50픽셀의 임시 이미지(png형식) 생성
    작성일:2023.06.13
    '''
    size = (50, 50)
    image = Image.new("RGBA", size)
    temp_img = BytesIO()
    image.save(temp_img, format="PNG")
    temp_img.name = "image.png"
    temp_img.seek(0)
    return temp_img


class ProductPostTest(APITestCase):
    '''
    작성자: 장소은
    내용: 일반유저가 상품 post 했을 때, admin유저가 post했을 때 testcode 작성
          다중이미지 업로드 기능 업데이트 
    작성일: 2023.06.07
    업데이트: 2023.06.23  
    '''
    @classmethod
    def setUpTestData(cls):
        date = timezone.now() + timedelta(seconds=random.randint(0, 86400))
        cls.user_data = {
            "email": "test@google.com",
            "username": "testuser",
            "password": "Xptmxm123@456"
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.admin = User.objects.create_superuser(
            email="adminuser@test.com", username="관리자소은", password="Xptmxm123@456")
        cls.admin_data = {"email": "adminuser@test.com",
                          "password": "Xptmxm123@456"}

        cls.faker = Faker()
        cls.category_data = {
            'category_name': "카테고리"
        }
        cls.category = ShopCategory.objects.create(**cls.category_data)
        cls.product_data = {
            'product_name': "상품",
            'product_desc': "테스트",
            'category': cls.category.id,
            'product_date': date,
            'product_price': 10000,
            'product_stock': 123,
            "images": [
                {
                    "id": 1,
                    "product": 1,
                    "image_file": ""
                }]
        }

        image_file = arbitrary_image()
        cls.product_data["images"][0]["image_file"] = image_file

    def setUp(self):
        self.admin_access_token = self.client.post(
            reverse('log_in'), self.admin_data).data['access']
        self.access_token = self.client.post(
            reverse('log_in'), self.user_data).data['access']

    def test_user_post_product(self):
        image_file = arbitrary_image()
        self.product_data["images"][0]["image_file"] = image_file
        self.product_data["uploaded_images"] = [image_file]
        url = reverse("category_sortby_product_view", kwargs={
                      "category_id": self.category.id})
        response = self.client.post(
            path=url,
            data=self.product_data,
            HTTP_AUTHORIZATION=f"Bearer {self.admin_access_token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_notadmin_post_product(self):
        response = self.client.post(
            path=reverse("category_sortby_product_view", kwargs={
                         "category_id": self.category.id}),
            data=self.product_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEquals(response.status_code, 403)


class ProductUpdateTest(APITestCase):
    '''
    내용 : 상품 수정 
    '''
    pass
