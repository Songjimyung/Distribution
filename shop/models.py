from django.db import models
from users.models import User
from django.urls import reverse


class ShopCategory(models.Model):
    '''
    작성자 : 장소은
    내용 : 상품 분류 카테고리 모델
    최초 작성일: 2023.06.06
    업데이트 일자:
    '''
    category_name = models.CharField(max_length=30)
    category_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.category_name)

    def get_absolute_url(self):
        return reverse('product_view', kwargs={"category_id": self.id})


class ShopProduct(models.Model):
    '''
    작성자 : 장소은
    내용 : 상품의 정보(이름,가격,수량,설명,등록일)를 나타내는 모델
    최초 작성일: 2023.06.06
    업데이트 일자:
    '''
    product_name = models.CharField(max_length=30)
    product_price = models.PositiveIntegerField(default=0)
    product_stock = models.PositiveIntegerField(default=0)
    product_desc = models.TextField()
    product_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        ShopCategory, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return str(self.product_name)


class ShopOrder(models.Model):
    '''
    작성자 : 장소은
    내용 : 주문 정보를 나타내는 모델
    최초 작성일: 2023.06.06
    업데이트 일자:
    '''
    order_quantity = models.PositiveIntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    zip_code = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    address_detail = models.CharField(max_length=100)
    address_message = models.CharField(max_length=150)
    receiver_name = models.CharField(max_length=20)
    receiver_number = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ShopOrderDetail(models.Model):
    '''
    작성자 : 장소은
    내용 : 주문의 상태를 나타내는 모델
    최초 작성일: 2023.06.06
    업데이트 일자:
    '''
    product_count = models.PositiveIntegerField(default=0)
    order_detail_status = models.CharField(max_length=10)
    order = models.ForeignKey(ShopOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE)
    # price = models.ForeignKey(Amount, on_delete=models.CASCADE)


class ShopImageFile(models.Model):
    '''
    작성자 : 장소은
    내용 : 상품 이미지 모델
    최초 작성일: 2023.06.06
    업데이트 일자:
    '''
    image_file = models.ImageField(null=True, blank=True)
    product = models.ForeignKey(
        ShopProduct, on_delete=models.CASCADE, related_name='images')
