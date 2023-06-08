import requests
from rest_framework import serializers
from .models import Payment
from shop.models import ShopProduct

class PaymentSerializer(serializers.ModelSerializer):
    '''
    작성자 : 송지명
    작성날짜 : 2023.06.06
    작성내용 : 결제 시스템 시리얼라이저
    Toss api에 결제 요청하여 받아오고 amount는 shopproduct의 price 를 상속.
    결제 후 Toss api의 response에서 payToken 값을 받아 저장(추후 환불 시 사용)
    
    업데이트 날짜 :
    '''
    
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    description = serializers.CharField(max_length=255)
    
    class Meta:
        model = Payment
        fields = ('amount','currency','description')
    