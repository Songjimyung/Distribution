from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, PaymentScheduleSerializer, RegisterPaymentSerializer
from .models import RegisterPayment, Payment
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
    


class ReceiptAPIView(APIView):
    '''
    작성자 : 송지명
    작성일 : 2023.06.12
    작성내용 : 결제 후 영수증 정보
    업데이트 날짜 :
    '''
    @csrf_exempt
    def get(self, request):
        iamport = Iamport(imp_key=settings.IMP_KEY, imp_secret=settings.IMP_SECRET)
        token = iamport.get_headers()   
        print(token)
        # data = json.loads(request.body)
        # merchant_uid = data.get('merchant_uid')
        merchant_uid = request.GET.get('merchant_uid')  # 쿼리 매개변수로 변경

        print(merchant_uid)
        receipt_url = f'https://api.iamport.kr/payments/find/{merchant_uid}'
        response = requests.get(receipt_url, headers=token)
        print(response)
        receipt_data = response.json()
        print(receipt_data)
        
        return JsonResponse(receipt_data)
    
