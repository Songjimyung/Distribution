from django.urls import path
from payments import views

urlpatterns = [    
    path('register/', views.RegisterCustomerView.as_view(), name='register_payment' ),
    path('schedule/', views.CreatePaymentScheduleView.as_view(), name='schedule_payment'),
    path('receipt/', views.ReceiptAPIView.as_view(), name='receipt_payment'),
]