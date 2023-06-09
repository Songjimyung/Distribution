from users.models import User
import requests
import os
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from users.serializers import (
    SignUpSerializer, CustomTokenObtainPairSerializer, CustomRefreshToken
)

BACK_BASE_URL = 'http://127.0.0.1:8000/'
FRONT_BASE_URL = 'http://127.0.0.1:5500/'
GOOGLE_CALLBACK_URI = BACK_BASE_URL + 'users/google/callback/'

state = os.environ.get("STATE")


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

def generate_jwt_token(user):
    refresh = CustomRefreshToken.for_user(user)
    
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}

# Google 로그인
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

def google_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')

    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        redirect_url = f'{FRONT_BASE_URL}/index.html'
        err_msg = "error"
        redirect_url_with_status = f'{redirect_url}?err_msg={err_msg}'
        
        return redirect(redirect_url_with_status)

    access_token = token_req_json.get('access_token')
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    
    if email_req_status != 200:
        redirect_url = f'{FRONT_BASE_URL}/index.html'
        err_msg = "failed_to_get"
        redirect_url_with_status = f'{redirect_url}?err_msg={err_msg}'
        
        return redirect(redirect_url_with_status)

    email_req_json = email_req.json()
    email = email_req_json.get('email')

    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user) 

        if social_user is None:
            redirect_url = f'{FRONT_BASE_URL}/index.html'
            status_code = 204
            redirect_url_with_status = f'{redirect_url}?status_code={status_code}'
            
            return redirect(redirect_url_with_status)

        if social_user.provider != 'google':
            redirect_url = f'{FRONT_BASE_URL}/index.html'
            status_code = 400
            redirect_url_with_status = f'{redirect_url}?status_code={status_code}'
            
            return redirect(redirect_url_with_status)

        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BACK_BASE_URL}users/google/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            redirect_url = f'{FRONT_BASE_URL}/index.html'
            err_msg = "failed_to_signin"
            redirect_url_with_status = f'{redirect_url}?err_msg={err_msg}'
            
            return redirect(redirect_url_with_status)

        jwt_token = generate_jwt_token(user)
        print("+ + + + + + + + + + +")
        print(jwt_token)
        print("+ + + + + + + + + + +")
        response = HttpResponseRedirect(f'{FRONT_BASE_URL}/index.html')
        response.set_cookie('jwt_token', jwt_token)
        
        return response

    except User.DoesNotExist:
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BACK_BASE_URL}users/google/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            redirect_url = f'{FRONT_BASE_URL}/index.html'
            err_msg = "google_signup"
            redirect_url_with_status = f'{redirect_url}?err_msg={err_msg}'
            
            return redirect(redirect_url_with_status)

        redirect_url = f'{FRONT_BASE_URL}/index.html'
        status_code = 201
        redirect_url_with_status = f'{redirect_url}?status_code={status_code}'
        
        return redirect(redirect_url_with_status)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client