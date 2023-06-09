from rest_framework import serializers
from campaigns.models import Campaign
from .models import Payment
from iamport import Iamport
from config import settings
import time
    
class RegisterSerializer(serializers.ModelSerializer):
    '''
    작성자 : 송지명
    작성날짜 : 2023.06.09
    작성내용 : 결제정보 등록 시리얼라이저
    Iamport api에 카드번호를 보내 customer_uid 요청.
    요청 후 Iamport api에서 데이터 값을 받아 저장(추후 예약 시 사용)
    
    업데이트 날짜 :
    '''
    expiry_at = serializers.CharField(error_messages={
            "required": "유효기간은 필수 입력 사항입니다!",
            "blank": "유효기간은 필수 입력 사항입니다!"
        }, write_only=True)
    birth = serializers.CharField(error_messages={
            "required": "유효기간은 필수 입력 사항입니다!",
            "blank": "유효기간은 필수 입력 사항입니다!"
        }, write_only=True)
    pwd_2digit = serializers.CharField(error_messages={
            "required": "유효기간은 필수 입력 사항입니다!",
            "blank": "유효기간은 필수 입력 사항입니다!"
        }, write_only=True)
    class Meta:
        model = Payment
        fields = ('created_at','customer_uid', 'card_number', 'expiry_at', 'birth', 'pwd_2digit')

    def create(self, data):
        get_expiry = data.get('expiry_at')
        birth = data.get('birth')
        pwd_2digit = data.get('pwd_2digit')
        iamport = Iamport(imp_key=settings.IMP_KEY, imp_secret=settings.IMP_SECRET)
        response = iamport.customer_create(
            customer_uid=self.context['request'].user.email,
            card_number=data['card_number'],
            expiry=get_expiry,
            birth=birth,
            pg='nice',
            pwd_2digit=pwd_2digit,
        )
        get_card_number = response.get('card_number')
        get_customer_uid = response.get('customer_uid')
        get_user = self.context['request'].user
        exist_card_number = Payment.objects.filter(card_number=get_card_number)
        
        if exist_card_number:
            raise serializers.ValidationError("이미 등록된 카드 번호입니다.")
        payment = Payment.objects.create(
            user=get_user,
            card_number=get_card_number,
            customer_uid=get_customer_uid            
        )
        return payment
    

class PaymentScheduleSerializer(serializers.Serializer):
    '''
    작성자 : 송지명
    작성날짜 : 2023.06.09
    작성내용 : 펀딩 결제용 시리얼라이저.
    캠페인 ID 및 결제 금액을 받아와 request user의 결제용 customer_uid 를 이용해 결제.
    추후 결제 취소를 위한 merchant_uid 저장.
    
    '''
    campaign_date = serializers.IntegerField(write_only=True)
    amount = serializers.CharField(max_length=10, write_only=True)
    class Meta:
        model = Payment
        fields = ('campaign_date','amount')
        
    def create(self, data):
        campaign = Campaign.objects.get(id=data.get('campaign_date'))
        
        date = campaign.campaign_end_date  
        schedules_date = date.replace(tzinfo=None)
        schedules_at = int(schedules_date.timestamp())
        request = self.context['request']
        iamport = Iamport(imp_key=settings.IMP_KEY, imp_secret=settings.IMP_SECRET)
        getcard = Payment.objects.get(pk=request.user.id)
        amount = data.get('amount')
        merchant_uid = f"imp{int(time.time())}"
        
        data = Payment.objects.filter(user=request.user, card_number=getcard.card_number).first()
        data.amount = amount
        data.merchant_uid = merchant_uid
        data.campaign_date = campaign
        data.save()
        customer_uid = data.customer_uid

        
        schedules = {
            "merchant_uid": merchant_uid,
            "schedule_at": schedules_at,
            "currency": "KRW",
            "amount": amount,
            "name": request.user.name
        }

        payload = {
            'customer_uid': customer_uid,
            'schedules': [schedules]
        }

        response=iamport.pay_schedule(**payload)
        print(response)

        return response
        
       