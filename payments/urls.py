from django.urls import path
from payments import views

urlpatterns = [    
    path('register/', views.RegisterCustomerView.as_view() ),
    path('schedule/', views.CreatePaymentScheduleView.as_view())
]