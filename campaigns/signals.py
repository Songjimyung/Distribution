from .models import Participant
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from users.models import Notification
from datetime import datetime, timedelta
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore

channel_layer = get_channel_layer()


def send_daily_notifications():
    '''
    작성자: 장소은
    내용: 현재 날짜로부터 3일 이내에 캠페인이 시작되는 경우 
          참가자에게 알림을 보내고, 보낸 알림 기록 

    최초 작성일: 2023.06.22
    '''
    current_datetime = timezone.now()
    campaign_start_date = current_datetime + timedelta(days=3)
    participants = Participant.objects.filter(
        is_participated=True,
        campaign__activity_start_date__lte=campaign_start_date
    )
    for participant in participants:
        print(current_datetime, participant.user.username)
        days_remain = (campaign_start_date - current_datetime).days
        message = {
            'type': 'notification_message',
            'message': f'캠페인 시작까지 {days_remain}일 남았습니다.',
        }
        async_to_sync(channel_layer.group_send)("notification_group", {
            'type': 'notification_message',
            'message': json.dumps(message)
        })

        # 알림 레코드 생성
        notification = Notification.objects.create(
            participant=participant,
            message=f'캠페인 시작까지 {days_remain}일 남았습니다.',
        )
        notification.save()


scheduler = BackgroundScheduler()

scheduler.add_jobstore(DjangoJobStore(), "djangojobstore")

# scheduler.add_job(send_daily_notifications, 'interval', minutes=1)  # 테스트용
scheduler.add_job(send_daily_notifications,
                  'cron',
                  hour=18
                  )  # 매일 오후 6시에 작업 실행 예약

register_events(scheduler)

scheduler.start()
