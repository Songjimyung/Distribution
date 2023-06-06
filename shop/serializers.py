from rest_framework.serializers import ValidationError
from rest_framework import serializers
from .models import ShopProduct
# from users.serializers import UserSerializer



class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = '__all__'
