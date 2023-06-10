from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, PaymentScheduleSerializer
from rest_framework import status


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