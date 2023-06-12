from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ShopProduct, ShopCategory
from .serializers import ProductListSerializer, ProductSerializer, CategoryListSerializer
from config.permissions import IsAdminUserOrReadonly
from django.core.exceptions import ValidationError
from django.http import JsonResponse


class ProductViewAPI(APIView):
    '''
    작성자:장소은
    내용: 카테고리별 상품목록 조회(일반,관리자) / 상품 등록(관리자) 
    작성일: 2023.06.06
    '''
    # permission_classes = [IsAdminUserOrReadonly]

    def get(self, request, category_id):
        category = get_object_or_404(ShopCategory, id=category_id)
        products = ShopProduct.objects.filter(category_id=category.id)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, category_id):
        category = get_object_or_404(ShopCategory, id=category_id)
        serializer = ProductListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(category=category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailViewAPI(APIView):
    '''
    작성자:장소은
    내용: 카테고리별 상품 상세 조회/ 수정 / 삭제 (일반유저는 조회만)
    작성일: 2023.06.06
    '''
    permission_classes = [IsAdminUserOrReadonly]

    def get(self, request, product_id):
        product = get_object_or_404(ShopProduct, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, product_id):
        product = get_object_or_404(ShopProduct, id=product_id)
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = get_object_or_404(ShopProduct, id=product_id)
        product.delete()
        return Response({"massage": "삭제 완료"}, status=status.HTTP_204_NO_CONTENT)


def category_list(request):
    categories = ShopCategory.objects.all()
    data = [{'category_id': category.id, 'category_name': category.category_name}
            for category in categories]
    return Response({"massage": "삭제 완료"}, status=status.HTTP_204_NO_CONTENT)


class AdminProductViewAPI(APIView):
    '''
    작성자 : 박지홍
    내용 : 어드민 페이지에서 전체 상품 목록을 받아오기위해 사용
    최초 작성일 : 2023.06.09
    업데이트 일자 :
    '''

    def get(self, request):
        products = ShopProduct.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminCategoryViewAPI(APIView):
    '''
    작성자 : 박지홍
    내용 : 어드민 페이지에서 전체 카테고리 목록을 받아오기위해 사용
    최초 작성일 : 2023.06.09
    업데이트 일자 :
    '''

    def get(self, request):
        categorys = ShopCategory.objects.all()
        serializer = CategoryListSerializer(categorys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
