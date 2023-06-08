from rest_framework.decorators import api_view
from rest_framework.response import Response
from config import settings
import json
from iamport import Iamport
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# iamport 설정

@api_view(['POST'])
def register_customer(request):
    '''
    작성자 : 송지명
    작성일 : 2023.06.08
    작성내용 : 유저의 카드 정보 등록. //email을 직접 입력할지 유저의 이메일을 받아올지.
    '''
    iamport = Iamport(imp_key = settings.IMP_KEY , imp_secret = settings.IMP_SECRET)

    data = json.loads(request.body)
    card_number = data.get('card_number')
    expiry = data.get('expiry')
    birth = data.get('birth')
    email = request.user.eamil
    pwd_2digit = data.get('pwd_2digit')

    if not all([card_number, expiry, birth, email]):
        return JsonResponse({'message': '입력값이 올바르지 않습니다.'}, status=400)

    try:
        response = iamport.customer_create(
            customer_uid=email,
            card_number=card_number,
            expiry=expiry,
            birth=birth,
            pg = 'nice',
            pwd_2digit = pwd_2digit,            
        )
        
        customer_uid = response.get('customer_uid')
        
        return Response(response)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)
  
@csrf_exempt
def create_payment_schedule(request):
    '''
    작성자 : 송지명
    작성일 : 2023.06.08
    작성내용 : 캠페인 펀딩 예약 결제 기능.// 아직 초안이라 json으로 데이터를 주고 있으나 
    customer_uid는 모델에서 받아서 사용, schedules는 캠페인쪽에서 받아서 사용할 예정.
    '''
    iamport = Iamport(imp_key= settings.IMP_KEY , imp_secret = settings.IMP_SECRET)
    data = json.loads(request.body)
    customer_uid = data.get('customer_uid')    
    schedules = data.get('schedules')
    payload = {
        'customer_uid': customer_uid,        
        'schedules': schedules
    }
    iamport.pay_schedule(**payload)
    
    return JsonResponse({'message':"결제완료"})