from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from .models import User, UserProfile

channel_layer = get_channel_layer()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''
    작성자 : 장소은
    내용 : 유저 생성 시 기본 프로필 자동 생성
    최초 작성일 : 2023.06.21
    '''
    if created:
        UserProfile.objects.create(user=instance)
