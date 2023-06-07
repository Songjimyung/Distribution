from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from users.serializers import SignUpSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)


class UserView(APIView):
    '''
    작성자 : 이주한
    내용 : 회원가입, 회원정보 수정, 회원 비활성화에 사용되는 view 클래스
    최초 작성일 : 2023.06.06
    업데이트 일자 :
    '''
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 회원정보 수정 PUT 메소드
    def put(self, request):
        pass

    # 회원 비활성화 DELETE 메소드
    def delete(self, request):
        pass


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer