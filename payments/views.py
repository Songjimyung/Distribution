from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from config import settings
from django.http import HttpResponse
import requests
import json
from iamport import Iamport
from django.http import JsonResponse


# iamport 설정
iamport = Iamport(imp_key = settings.IMP_KEY , imp_secret = settings.IMP_SECRET)

@api_view(['POST'])
def register_customer(request):
    try:
        data = json.loads(request.body)
        card_number = data.get('card_number')
        expiry = data.get('expiry')
        birth = data.get('birth')
        email = data.get('email')
    except :
        return JsonResponse({'message': '에러'}, status=400)
    
    try:
        iamport.customer_create(
            customer_uid=email,
            card_number=card_number,
            expiry=expiry,
            birth=birth,
        )
    except :
        return JsonResponse({'message': '에러'}, status=400)
  

def create_payment_schedule(customer_uid, merchant_uid, amount, schedule_at):
    url = 'https://api.iamport.kr/subscribe/payments/schedule'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'YOUR_API_KEY',
    }
    payload = {
        'customer_uid': customer_uid,
        'merchant_uid': merchant_uid,
        'amount': amount,
        'schedule_at': schedule_at,
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        # 결제 스케줄 등록 성공
        return True
    else:
        # 결제 스케줄 등록 실패
        return False

        
