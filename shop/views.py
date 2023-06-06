from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ShopProduct, ShopCategory
from .serializers import ProductListSerializer
from config.permissions import IsAdminUserOrReadonly



class ProductViewAPI(APIView): 
    '''
    작성자:장소은
    내용: 관리자용 카테고리별 상품목록 조회 / 상품 등록 
    작성일: 2023.06.06
    
    '''
    permission_classes = [IsAdminUserOrReadonly]

    def get(self, request, category_name):
        category = get_object_or_404(ShopCategory, category_name=category_name)
        products = ShopProduct.objects.filter(category=category)
        serializer = ProductListSerializer(products, many=True)
        return Response(status=status.HTTP_200_OK)

    def post(self, request, category_name):
        category = get_object_or_404(ShopCategory, category_name=category_name)
        serializer = ProductListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 카테고리별 상품 상세 조회 / 수정 / 삭제 
