from rest_framework.serializers import ValidationError
from rest_framework import serializers
from .models import ShopProduct


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = ('product_name', 'product_price', 'product_desc')