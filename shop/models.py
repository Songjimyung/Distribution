from django.db import models
from users.models import User


'''
작성자 : 장소은
내용 : 상품 분류 카테고리 모델
최초 작성일: 2023.06.06
업데이트 일자:
'''
class Shop_Category(models.Model):
    category_name = models.CharField(max_length=30)


'''
작성자 : 장소은
내용 : 상품의 정보(이름,가격,수량,설명,등록일)를 나타내는 모델
최초 작성일: 2023.06.06
업데이트 일자:
'''
class Shop_Product(models.Model):
    product_name = models.CharField(max_length=30)
    product_price = models.PositiveIntegerField(default=0)
    product_stack = models.PositiveIntegerField(default=0)
    product_desc = models.TextField()
    product_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Shop_Category, on_delete=models.CASCADE, related_name='products')


'''
작성자 : 장소은
내용 : 장바구니 모델 
최초 작성일: 2023.06.06
업데이트 일자:
'''
class Shop_Cart:
    product_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shop_Product, on_delete=models.CASCADE)


'''
작성자 : 장소은
내용 : 주문 정보를 나타내는 모델
최초 작성일: 2023.06.06
업데이트 일자:
'''
class Shop_Order:
    oder_date = models.DateTimeField(auto_now_add=True)
    zip_code = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    address_detail = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=20)
    receiver_number = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


'''
작성자 : 장소은
내용 : 주문의 상태를 나타내는 모델
최초 작성일: 2023.06.06
업데이트 일자:
'''
class Shop_OrderDetail:
    product_count = models.PositiveIntegerField(default=0)
    order_detail_status = models.CharField(max_length=10)
    order = models.ForeignKey(Shop_Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Shop_Product, on_delete=models.CASCADE)
    # price = models.ForeignKey(Amount, on_delete=models.CASCADE)


'''
작성자 : 장소은
내용 : 상품 이미지 모델
최초 작성일: 2023.06.06
업데이트 일자:
'''
class Shop_ImageFile:
    image_file = models.ImageField(null=True, blank=True)
    product = models.ForeignKey(Shop_Product, on_delete=models.CASCADE)
