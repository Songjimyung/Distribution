from django.urls import path
from users import views


urlpatterns = [
    # 회원가입
    path('signup/', views.UserView.as_view(), name='sign_up'),
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('oauth/kakao/callback/', views.kakaoCallBackView.as_view(), name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
    # 로그인
    path('login/', views.CustomTokenObtainPairView.as_view(), name='log_in'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('list/', views.UserListView().as_view(), name='user_list'),
    path('<int:user_id>/', views.UserDetailView().as_view(), name='user'),
]
