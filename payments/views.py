from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, PaymentScheduleSerializer
from rest_framework import status
from iamport import Iamport
from config import settings
import requests, json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# iamport 설정

class RegisterCustomerView(APIView):
    '''
    작성자 : 송지명
    작성일 : 2023.06.08
    작성내용 : 유저의 카드 정보 등록.
    '''

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def get(self, request):
        serializer = RegisterSerializer()
        token = serializer.get_token()
        print(token)
        return Response({'token': token})
  
class CreatePaymentScheduleView(APIView):
    '''
    작성자 : 송지명
    작성일 : 2023.06.08
    작성내용 : 캠페인 펀딩 예약 결제 기능.
    '''

    def post(self, request):
        serializer = PaymentScheduleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            response =serializer.save()
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class PaymentView(APIView):
#     def post(self, request):
        
#     def get(self, request) :
@csrf_exempt
def receipt(request):
    iamport = Iamport(imp_key=settings.IMP_KEY, imp_secret=settings.IMP_SECRET)
    token = iamport.get_headers()   
    print(token)
    data = json.loads(request.body)
    merchant_uid = data.get('merchant_uid')
    print(merchant_uid)
    receipt_url = f'https://api.iamport.kr/payments/find/{merchant_uid}'
    response = requests.get(receipt_url, headers=token)
    print(response)
    receipt_data =response.json()
    print(receipt_data)
    
    return JsonResponse(receipt_data)