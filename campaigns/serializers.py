from rest_framework import serializers
from users.models import User
from campaigns.models import (
    Campaign, 
    CampaignComment, 
    CampaignReview, 
    Funding, 
    FundingOrder
)


class CampaignSerializer(serializers.ModelSerializer):
    """
    작성자 : 최준영
    내용 : 캠페인 시리얼라이저 입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    class Meta:
        model = Campaign
        fields = "__all__"


class CampaignCreateSerializer(serializers.ModelSerializer):
    """
    작성자 : 최준영
    내용 : 캠페인 생성 시리얼라이저 입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    class Meta:
        model = Campaign
        fields = (
            "title",
            "content",
            "members",
            "current_members",
            "startdate",
            "enddate",
            "image",
            "is_funding",
            "status",
        )
