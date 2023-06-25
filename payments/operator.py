from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from django.conf import settings
from .views import DetailScheduleReceiptAPIView
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import register_events


def start():
    """
    작성자 : 송지명
    내용 : Payment의 status를 Campaign status 체크 후 변경 실행해주는 메서드.
    최초 작성일 : 2023.06.24
    업데이트 일자 :
    """
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "djangojobstore")
    register_events(scheduler)
    # 매분 8초에 실행되도록 테스트
#     @scheduler.scheduled_job(CronTrigger(hour=8))
    @scheduler.scheduled_job("cron", second="1", name="check")
    def check():
         DetailScheduleReceiptAPIView().check_payment_status()

    scheduler.start()
