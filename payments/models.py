from django.db import models
from users.models import User
from campaigns.models import Campaign


class Payment(models.Model):
    '''
    작성자 : 송지명
    작성날짜 : 2023.06.06
    작성내용 : 결제 시스템 모델
    업데이트 날짜 :
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount= models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_uid = models.CharField(max_length=255, blank=True, null=True)
    card_number = models.CharField(max_length=25)
    campaign_date = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    merchant_uid = models.CharField(max_length=255, blank=True, null=True)
