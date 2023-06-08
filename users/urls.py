from django.urls import path
from users import views


urlpatterns = [
    # 회원가입
    path('signup/', views.UserView.as_view(), name='sign_up'),
    
    # 로그인
    path('login/', views.CustomTokenObtainPairView.as_view(), name='log_in'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
]