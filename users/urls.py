from django.urls import path
from users import views
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    # 회원가입
    path('signup/', views.UserView.as_view(), name='sign_up'),
    
    # 로그인
    path('login/', TokenObtainPairView.as_view(), name='log_in'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]