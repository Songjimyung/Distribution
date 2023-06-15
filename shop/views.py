from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ShopProduct, ShopCategory, ShopOrder, ShopOrderDetail
from .serializers import (
    ProductListSerializer, CategoryListSerializer, OrderProductSerializer, OrderDetailSerializer
)
from config.permissions import IsAdminUserOrReadonly


class ProductViewAPI(APIView):
    '''
    작성자:장소은
    내용: 카테고리별 상품목록 조회(일반,관리자) / 상품 등록(관리자) 
    작성일: 2023.06.06
    '''
    permission_classes = [IsAdminUserOrReadonly]

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
        serializer = ProductListSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, product_id):
        product = get_object_or_404(ShopProduct, id=product_id)
        serializer = ProductListSerializer(
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


class CategoryViewAPI(APIView):
    '''
    작성자 : 장소은
    내용 : 어드민 페이지에서 카테고리 생성할 때 사용
    최초 작성일 : 2023.06.12
    업데이트 일자 :
    '''

    def post(self, request):
        serializer = CategoryListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderProductViewAPI(APIView):
    '''
    작성자 : 장소은
    내용 : 해당 상품에 대한 주문 생성 / 사용자가 proudct_id에 해당하는 상품 목록 조회 
    최초 작성일 : 2023.06.13
    업데이트 일자 :
    '''

    def get(self, request, product_id):
        orders = ShopOrder.objects.filter(
            user=request.user.id, product_id=product_id)
        serializer = OrderProductSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        product = get_object_or_404(ShopProduct, id=product_id)
        serializer = OrderProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailViewAPI(APIView):
    '''
    작성자 : 장소은
    내용 : order_id에 대한 주문 상세 조회(주문내역) class
    최초 작성일 : 2023.06.13
    업데이트 일자 :
    '''

    def get(self, request, order_id):
        order = get_object_or_404(ShopOrder, id=order_id)
        serializer = OrderProductSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminOrderViewAPI(APIView):
    '''
    작성자 : 장소은
    내용 : 어드민 페이지에서 해당 상품에 대한 모든 주문내역 조회
    최초 작성일 : 2023.06.09
    업데이트 일자 :
    '''

    def get(self, request, product_id):
        orders = ShopOrder.objects.filter(product_id=product_id)
        serializer = OrderProductSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MypageOrderViewAPI(APIView):
    '''
    작성자 : 장소은
    내용 : 마이페이지에서 유저의 모든 주문내역 조회
    최초 작성일 : 2023.06.14
    업데이트 일자 :
    '''

    def get(self, request):
        orders = ShopOrder.objects.filter(user=request.user.id)
        serializer = OrderProductSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductRecentListViewAPI(APIView):
    '''
    작성자:장소은
    내용: 최신 상품 목록 조회 API
    작성일: 2023.06.15
    '''

    def get(self, request):
        products = ShopProduct.objects.all().order_by('-product_date')
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
