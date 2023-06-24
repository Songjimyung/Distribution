
from chat.models import Room
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from users.models import Notification
from django.utils import timezone

channel_layer = get_channel_layer()


def send_admin_notifications(room_id):
    '''
    작성자 : 장소은
    내용 : 채팅 룸이 생성되고 상담이 진행중이지 않은 채팅 룸에 대해서 관리자에게 실시간 알림 기능 
    최초 작성일 : 2023.06.22
    '''
    message = {
        'type': 'send_admin_notification',
        'room_id': room_id,
        'message': '새로운 채팅요청이 있습니다.',
    }
    async_to_sync(channel_layer.group_send)("notification_admin_group", {
        'type': 'send_admin_notification',
        'message': json.dumps(message)
    })
