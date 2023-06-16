from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, PaymentScheduleSerializer, RegisterPaymentSerializer
from .models import RegisterPayment, Payment
from shop.models import ShopProduct
from users.models import User
from rest_framework import status
from iamport import Iamport
from config import settings
import requests, json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class RegisterCustomerView(APIView):
    
    def post(self, request):
        '''
        작성자 : 송지명
        작성일 : 2023.06.08
        작성내용 : 유저의 카드 정보 등록.
        업데이트날짜 : 2023.06.13
        '''
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        '''
        작성자 : 송지명
        작성일 : 2023.06.13
        작성내용 : 유저의 카드정보 조회 
        업데이트날짜 : 
        '''
        register_payments = RegisterPayment.objects.filter(user=request.user)
        serializer = RegisterPaymentSerializer(register_payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        
        card_id = request.data.get('id')
        register_payments = RegisterPayment.objects.get(user=request.user, id = card_id)
        if register_payments:           
            register_payments.delete()
            return Response({"message": "카드정보 삭제 성공"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "카드정보 없음"}, status=status.HTTP_404_NOT_FOUND)
        
        
    
        

class CreatePaymentScheduleView(APIView):
    
    def post(self, request):
        '''
        작성자 : 송지명
        작성일 : 2023.06.08
        작성내용 : 캠페인 펀딩 예약 결제 기능.
        업데이트 날짜 : 2023.06.14
        '''
        serializer = PaymentScheduleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        '''
        작성자 : 송지명
        작성일 : 2023.06.13
        작성내용 : 예약 결제 후 예약 정보 조회, 예약정보 없을 경우 데이터 삭제
        업데이트 날짜 : 
        '''
        iamport = Iamport(imp_key=settings.IMP_KEY, imp_secret=settings.IMP_SECRET)
        token = iamport.get_headers()
        print(request.user.id)
        users = Payment.objects.filter(user=request.user.id)
        receipt_data_list = []
        for user in users :
            merchant_uid = user.merchant_uid
            print(merchant_uid)
            receipt_url = f'https://api.iamport.kr/subscribe/payments/schedule/{merchant_uid}'
            response = requests.get(receipt_url, headers=token)
            if response.status_code == 200: 
                receipt_data = response.json()
                print(receipt_data)
                receipt_data_list.append(receipt_data)
            else:
                print(response)
                user.delete()
            
        return JsonResponse(receipt_data_list, safe=False)
    


class ScheduleReceiptAPIView(APIView):
    '''
    작성자 : 송지명
    작성일 : 2023.06.12
    작성내용 : 예약결제 후 영수증 정보
    업데이트 날짜 :
    '''
    @csrf_exempt
    def get(self, request):
        iamport = Iamport(imp_key=settings.IMP_KEY, imp_secret=settings.IMP_SECRET)
        token = iamport.get_headers()   
        merchant_uid = request.GET.get('merchant_uid')  # 쿼리 매개변수로 변경

        print(merchant_uid)
        receipt_url = f'https://api.iamport.kr/payments/find/{merchant_uid}'
        response = requests.get(receipt_url, headers=token)
        print(response)
        receipt_data = response.json()
        print(receipt_data)
        
        return JsonResponse(receipt_data)
    
class ReceiptAPIView(APIView):
    
    def post(self, request, user_id):
        '''
        작성자 : 송지명
        작성일 : 2023.06.14
        작성내용: 결제 후 모델에 저장
        업데이트 날짜 :
        '''
        merchant_uid = request.data.get('merchant_uid')
        imp_uid = request.data.get('imp_uid')
        amount = request.data.get('amount')
        product = request.data.get('product')
        print(user_id)
        user_data = User.objects.get(id=user_id)
        product_data = ShopProduct.objects.get(id=product)
        response = Payment.objects.create(user=user_data, amount=amount, imp_uid=imp_uid,merchant_uid=merchant_uid, product=product_data)
        response_data = {
            'user': user_data.username,
            'merchant_uid': response.merchant_uid,
            'imp_uid': response.imp_uid,
            'amount': response.amount,
            'product': response.product.product_name
            
        }
        print(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def get(self, request, user_id):
        '''
        작성자 : 송지명
        작성일 : 2023.06.14
        작성내용 : 유저의 결제정보 조회// 기존에는 iamport에 직접 조회였으나 모델에서 조회로 변경. 
                  상세 정보 조회 시 프론트에서 iamport로 요청 보내서 확인.
        업데이트 날짜 : 2023.06.15
        '''
        # iamport = Iamport(imp_key=settings.IMP_KEY, imp_secret=settings.IMP_SECRET)
        # token = iamport.get_headers()
        # merchant_uid = request.GET.get('merchant_uid')
        # imp_uid = request.GET.get('imp_uid')
        # receipt_url = "https://api.iamport.kr/payments"
        # params = {
        #     'merchant_uid' : merchant_uid,
        #     'imp_uid' : imp_uid
        # }
        # response = requests.get(receipt_url, params, headers=token)
        # response_data =response.json()
        # return JsonResponse(response_data)
        # user = User.objects.get(id=user_id)
        receipts = Payment.objects.filter(user=user_id, product__isnull=False)
        
        receipt_data = []
        for receipt in receipts :
            receipt_data.append({
                'user' : receipt.user.username,
                'amount': receipt.amount,
                'created_at': receipt.created_at,
                'product' : receipt.product.product_name,
                'imp_uid' : receipt.imp_uid,
                'merchant_uid' :receipt.merchant_uid
            })
        print(receipt_data)
        return JsonResponse(receipt_data, safe=False)