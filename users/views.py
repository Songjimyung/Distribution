from users.models import User
import requests
import os
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from users.serializers import SignUpSerializer, CustomTokenObtainPairSerializer


state = os.environ.get('STATE')
kakao_callback_uri = os.environ.get('KAKAO_CALLBACK_URI')
google_callback_uri = os.environ.get('GOOGLE_CALLBACK_URI')
base_url = os.environ.get('BASE_URL')
front_base_url = os.environ.get('FRONT_BASE_URL')


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

def generate_jwt_token(user):
    refresh = CustomRefreshToken.for_user(user)
    
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


# Google 로그인
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={google_callback_uri}&scope={scope}")

def google_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')

    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={google_callback_uri}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        redirect_url = f'{front_base_url}index.html'
        err_msg = "error"
        redirect_url_with_status = f'{redirect_url}?err_msg={err_msg}'
        
        return redirect(redirect_url_with_status)

    access_token = token_req_json.get('access_token')
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    
    if email_req_status != 200:
        redirect_url = f'{front_base_url}index.html'
        err_msg = "failed_to_get"
        redirect_url_with_status = f'{redirect_url}?err_msg={err_msg}'
        
        return redirect(redirect_url_with_status)

    email_req_json = email_req.json()
    email = email_req_json.get('email')

    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user) 

        if social_user is None:
            redirect_url = f'{front_base_url}index.html'
            status_code = 204
            redirect_url_with_status = f'{redirect_url}?status_code={status_code}'
            
            return redirect(redirect_url_with_status)

        if social_user.provider != 'google':
            redirect_url = f'{front_base_url}index.html'
            status_code = 400
            redirect_url_with_status = f'{redirect_url}?status_code={status_code}'
            
            return redirect(redirect_url_with_status)

        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{base_url}users/google/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            redirect_url = f'{front_base_url}index.html'
            err_msg = "failed_to_signin"
            redirect_url_with_status = f'{redirect_url}?err_msg={err_msg}'
            
            return redirect(redirect_url_with_status)

        jwt_token = generate_jwt_token(user)
        response = HttpResponseRedirect(f'{front_base_url}index.html')
        response.set_cookie('jwt_token', jwt_token)
        
        return response

    except User.DoesNotExist:
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{base_url}users/google/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            redirect_url = f'{front_base_url}index.html'
            err_msg = "google_signup"
            redirect_url_with_status = f'{redirect_url}?err_msg={err_msg}'
            
            return redirect(redirect_url_with_status)

        redirect_url = f'{front_base_url}index.html'
        status_code = 201
        redirect_url_with_status = f'{redirect_url}?status_code={status_code}'
        
        return redirect(redirect_url_with_status)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = google_callback_uri
    client_class = OAuth2Client


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
