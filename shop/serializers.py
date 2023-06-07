from rest_framework.serializers import ValidationError
from rest_framework import serializers
from .models import ShopProduct
# from users.serializers import UserSerializer



class ProductListSerializer(serializers.ModelSerializer):
    '''
    작성자:장소은
    내용: 카테고리별 상품목록 조회시 필요한 Serializer 클래스
    작성일: 2023.06.07
    '''
    class Meta:
        model = ShopProduct
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    '''
    작성자:장소은
    내용: 카테고리별 상품 상세 조회시 필요한 Serializer 클래스
    작성일: 2023.06.07
    '''
    class Meta:
        model = ShopProduct
        fields = ('product_name', 'product_price', 'product_desc')