from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from .models import ShopProduct, ShopCategory
from faker import Faker

class ProductTest(APITestCase):
    '''
    작성자: 장소은
    내용: 일반유저가 상품 post 했을 때, admin유저가 post했을 때 testcode 작성
    작성일: 2023.06.07
    '''
    @classmethod
    def setUpTestData(cls):
        cls.username = User.objects.create_user(email="testuser@test.com", username="장소은", password="Xptmxm123@456")
        cls.user_data = {"email": "testuser@test.com", "password": "Xptmxm123@456"}
        cls.admin = User.objects.create_superuser(email="adminuser@test.com", username="관리자소은", password="Xptmxm123@456")
        cls.admin_data = {"email": "adminuser@test.com", "password": "Xptmxm123@456"}
        cls.faker = Faker()
        cls.category = ShopCategory.objects.create(category_name=cls.faker.word(), category_number=1)
        cls.product = ShopProduct.objects.create(product_name=cls.faker.word(), product_desc=cls.faker.sentence(), product_price=1000, category=cls.category)
        cls.product_data = {'product_name':cls.product.product_name, 'product_desc':cls.product.product_desc, 'category':cls.category.id}


    def setUp(self): 
        self.admin_access_token = self.client.post(reverse('log_in'), self.admin_data).data['access']
        self.access_token = self.client.post(reverse('log_in'), self.user_data).data['access']


    def test_user_post_product(self):
        response = self.client.post(
            path=reverse("product_view", kwargs={"category_id":self.category.id}),
            data=self.product_data,
            HTTP_AUTHORIZATION=f"Bearer {self.admin_access_token}",
            )
        self.assertEquals(response.status_code, 201)


    def test_admin_post_product(self):
        response = self.client.post(
            path=reverse("product_view", kwargs={"category_id":self.category.id}),
            data=self.product_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            )
        self.assertEquals(response.status_code, 403)
