from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from users.serializers import SignUpSerializer, CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialAccount
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.shortcuts import redirect
from json.decoder import JSONDecodeError
from django.http import JsonResponse, HttpResponseRedirect
from django.http import HttpResponse
import requests
import os
from .models import User

state = os.environ.get('STATE')
kakao_callback_uri = os.environ.get('KAKAO_CALLBACK_URI')
base_url = os.environ.get('BASE_URL')
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


class CustomRefreshToken(RefreshToken):
    '''
    작성자 : 장소은
    내용 : 사용자에 대한 새로운 토큰을 생성하는 클래스. 사용자의 ID와 이메일 정보를 토큰에 추가하여 반환
    최초 작성일 : 2023.06.08
    업데이트 일자 :
    '''
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token["user_id"] = user.id
        token['email'] = user.email
        return token


def generate_jwt_token(user):
    '''
    작성자 : 장소은
    내용: 사용자를 인자로 받아 RefreshToken을 생성. 'refresh'와 'access'라는 키로 구성된 딕셔너리 형태의 문자열 토큰 반환
    최초 작성일 : 2023.06.08
    업데이트 일자 :
    '''
    refresh = CustomRefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


def kakao_login(request):
    '''
    작성자 : 장소은
    내용: client_id, redirect uri 등과 같은 정보를 url parameter로 함께 보내서 Redirect한다. Callback URI로 Code값이 들어가게 된다.
    최초 작성일 : 2023.06.08
    업데이트 일자 :
    '''
    rest_api_key = os.environ.get('KAKAO_REST_API_KEY')
    return redirect(
    f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={kakao_callback_uri}&response_type=code")


class kakaoCallBackView(APIView):
    '''
    작성자 : 장소은
    내용: Kakao 로그인 콜백을 처리하는 APIView GET. Kakao 토큰 API에 POST 요청을 보냄. 응답을 받아와서 JSON 형식으로 파싱하여 access_token추출
          응답 데이터에 'error' 키가 포함되어 있다면 에러처리. 
          그렇지 않은 경우는 access_token을 사용하여 Kakao API를 호출하여 사용자 정보를 가져옴 이메일(kakao_email), 연령대(age_range), 성별(gender) 추출
          try-except - 기존에 가입된 유저인지 체크
          만약 가입된 유저라면, 해당 유저정보를 사용하여 JWT 토큰을 생성하고, 리다이렉트 응답&JWT 토큰은 쿠키에 저장해 전달
          User.DoesNotExist - 새로운 가입자 처리, 가입 처리 결과에 따라 리다이렉트 응답을 생성
    최초 작성일 : 2023.06.08
    업데이트 일자 :
    '''
    def get(self, request):
        code = request.GET.get("code")
        rest_api_key = os.environ.get('KAKAO_REST_API_KEY')
        data = {
          "grant_type" : "authorization_code",
          "client_id" : rest_api_key,
          "redirection_url" : kakao_callback_uri,
          "code" : request.GET.get("code")
        }
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        response = requests.post(kakao_token_api, data=data)
        response_data = response.json()
        access_token = response_data.get("access_token")

        if "error" in response_data:
            error = response_data["error"]
            raise Exception(f"Access Token Request Error: {error}")
        profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
        profile_json = profile_request.json()
        kakao_user_info = profile_json.get('kakao_account')
        kakao_email = kakao_user_info["email"]
        age_range = kakao_user_info["age_range"]
        gender = kakao_user_info["gender"]
        
        try:
            user = User.objects.get(email=kakao_email)
            social_user = SocialAccount.objects.get(user=user) 
            # 기존에 kakao로 가입된 유저
            data = {'access_token': access_token, 'code': code}
            accept = requests.post(
                f"{base_url}users/kakao/login/finish/", data=data)
            jwt_token = generate_jwt_token(user)
            print(jwt_token)
            response = HttpResponseRedirect("http://127.0.0.1:3000/")
            response.set_cookie('jwt_token', jwt_token, path='/')
            return response
            # return JsonResponse(response_data)

        except User.DoesNotExist:
            data = {'access_token': access_token, 'code': code}
            accept = requests.post(
                f"{base_url}users/kakao/login/finish/", data=data)
            accept_status = accept.status_code

            if accept_status != 200:
                redirect_url = 'http://127.0.0.1:3000/index.html'
                status_code = accept_status
                err_msg = "kakao_signup"
                redirect_url_with_status = f'{redirect_url}?err_msg={err_msg}'
                return redirect(redirect_url_with_status)

            redirect_url = 'http://127.0.0.1:3000/index.html'
            status_code = 201
            redirect_url_with_status = f'{redirect_url}?status_code={status_code}'
            return redirect(redirect_url_with_status)


class KakaoLogin(SocialLoginView):
    '''
    작성자 : 장소은
    내용: Kakao OAuth2 어댑터와 OAuth2Client를 사용하여 Kakao 로그인을 처리하는 클래스. 인증 완료 후 SocialLoginView에서 처리되는 방식
    작성일 : 2023.06.08
    업데이트 일자 :
    '''
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = kakao_callback_uri


class UserListView(APIView):
    '''
    작성자 : 박지홍
    내용: 어드민 페이지에서 전체 일반 유저 리스트를 받기 위해 사용 
    작성일 : 2023.06.09
    업데이트 일자 :
    '''
    def get(self, request):
        users = User.objects.filter(is_admin=False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    '''
    작성자 : 박지홍
    내용: 어드민 페이지에서 일반 유저의 상세 정보를 알기 위해 사용
    작성일 : 2023.06.09
    업데이트 일자 :
    '''
    def get(self, request, user_id):
        user = User.objects.filter(id=user_id)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
