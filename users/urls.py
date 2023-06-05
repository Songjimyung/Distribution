from django.urls import path
from users import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)


urlpatterns = [    
    path('main/',  TokenObtainPairView.as_view(), name='main'),   

]