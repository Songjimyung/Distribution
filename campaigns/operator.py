from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from datetime import datetime, timedelta
from django.utils import timezone
from django.apps import AppConfig
from django.conf import settings
from .models import Participant, Campaign
from .views import check_campaign_status
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import register_events


def start():
    """
    작성자 : 최준영
    내용 : 캠페인 status 체크 실행 함수입니다.
    Blocking이 아닌 BackgroundScheduler를 활용하여 백그라운드에서 작동합니다.
    minute = '*/1' 로 1분마다 스케줄러 발동시켜 테스트해볼 수 있습니다.
    @scheduler.scheduled_job('cron', hour = '0', minute = '1', name = 'check')
    위 코드로 매일 1시에 스케줄링하도록 할 예정이나, 테스트는 아직 못해봤습니다.
    최초 작성일 : 2023.06.08
    업데이트 일자 :
    """
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "djangojobstore")
    register_events(scheduler)

    # @scheduler.scheduled_job('cron', minute = '*/1', name = 'check')
    @scheduler.scheduled_job("cron", hour="1", name="check")
    def check():
        check_campaign_status()

    scheduler.start()


