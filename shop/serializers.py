from rest_framework.serializers import ValidationError
from rest_framework import serializers
from .models import ShopProduct, ShopCategory, ShopImageFile


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopImageFile
        fields = ['id', 'product', 'image_file']


class ProductListSerializer(serializers.ModelSerializer):
    '''
    작성자:장소은
    내용: 카테고리별 상품목록 조회시 필요한 Serializer 클래스
    작성일: 2023.06.07
    '''
    images = PostImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(child=serializers.ImageField(
        max_length=1000000, allow_empty_file=False, use_url=False), write_only=True
    )

    class Meta:
        model = ShopProduct
        fields = ['id', 'product_name', 'product_price', 'product_stock',
                        'product_desc', 'product_date', 'category', 'images', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        product = super().create(validated_data)
        for image in uploaded_images:
            ShopImageFile.objects.create(image_file=image, product=product)
        return product


class ProductSerializer(serializers.ModelSerializer):
    '''
    작성자:장소은
    내용: 카테고리별 상품 상세 조회시 필요한 Serializer 클래스
    작성일: 2023.06.07
    '''
    class Meta:
        model = ShopProduct
        fields = ('product_name', 'product_price', 'product_desc')


class CategoryListSerializer(serializers.ModelSerializer):
    '''
    작성자:박지홍
    내용: 카테고리별 조회시 필요한 Serializer 클래스
    작성일: 2023.06.09
    '''
    class Meta:
        model = ShopCategory
        fields = '__all__'
