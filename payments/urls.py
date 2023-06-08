from django.urls import path
from payments import views
from .views import register_customer

urlpatterns = [    
    path('register/', register_customer ),
]