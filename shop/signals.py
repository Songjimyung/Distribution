from .models import RestockNotification, ShopProduct
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

channel_layer = get_channel_layer()


@receiver(post_save, sender=ShopProduct)
def send_notifications(sender, instance, created, **kwargs):
    '''
    작성자 : 장소은
    내용 : 상품이 재입고 된 경우 재입고 알림신청을 한 사용자들에게 알림 기능
    최초 작성일 : 2023.06.20
    '''
    if not created and instance.restocked:
        restock_notifications = RestockNotification.objects.filter(
            product=instance)
        for notification in restock_notifications:
            user = notification.user
            message = {
                'type': 'restock_notification',
                'message': f'상품 {instance.name}이(가) 재입고되었습니다.',
            }
            async_to_sync(channel_layer.group_send)("restock_notifications", {
                'type': 'send_notification',
                'message': json.dumps(message)
            })
