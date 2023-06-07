from django.contrib import admin
from campaigns.models import (
    Campaign, 
    CampaignComment, 
    CampaignReview, 
    Funding, 
    FundingOrder
)


@admin.register(Campaign)
class CampaignDisplay(admin.ModelAdmin):
    """
    작성자 : 최준영
    내용 : 캠페인 admin 페이지 등록 클래스입니다.
    list_display는 ManyToManyField를 지원하지 않아 like는 넣지 않았습니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    list_display = [
        'user',
        'title',
        'content',
        'members',
        'current_members',
        'startdate',
        'enddate',
        'created_at',
        'updated_at',
        'image',
        'is_funding',
        'status',
    ]
    fields = [
        'movie',
        'user',
        'content',
        'rating',
        'like',
    ]
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    list_filter = [
        'title',
        'user',
        'is_funding',
        'status',
    ]
    search_fields = [
        'title',
        'user',
        'content',
    ]


@admin.register(Funding)
class FundingDisplay(admin.ModelAdmin):
    """
    작성자 : 최준영
    내용 : 펀딩 admin 페이지 등록 클래스입니다.
    최초 작성일 : 2023.06.07
    업데이트 일자 : 
    """
    list_display = [
        'campaign',
        'funding_startdate',
        'deadline',
        'goal',
        'current',
        'approvefile',
        'created_at',
        'updated_at',
    ]
    fields = [
        'campaign',
        'funding_startdate',
        'deadline',
        'goal',
        'current',
        'approvefile',
    ]
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    list_filter = [
        'campaign',
        'funding_startdate',
        'deadline',
    ]
    search_fields = [
        'campaign',
        'funding_startdate',
        'deadline',
        'goal',
        'current',
        'approvefile',
        'created_at',
        'updated_at',
    ]
