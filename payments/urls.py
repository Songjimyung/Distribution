from django.urls import path
from payments import views
from .views import register_customer, create_payment_schedule

urlpatterns = [    
    path('register/', register_customer ),
    path('schedule/', create_payment_schedule)
]