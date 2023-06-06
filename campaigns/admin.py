from django.contrib import admin
from campaigns.models import (
    Campaign, 
    CampaignComment, 
    CampaignReview, 
    Funding, 
    FundingOrder
)


@admin.register(Campaign)
class ReviewDisplay(admin.ModelAdmin):
    """
    작성자 : 최준영
    내용 : 캠페인 admin 등록 클래스입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    # list_display는 ManyToManyField 미지원
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