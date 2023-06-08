from rest_framework import serializers
from users.models import User
from campaigns.models import (
    Campaign, 
    CampaignReview, 
    CampaignComment, 
    Funding, 
    FundingOrder
)


class BaseSerializer(serializers.ModelSerializer):
    """
    작성자 : 최준영
    내용 :  베이스 시리얼라이저입니다.
    중복되는 속성인 created_at과 updated_at을
    상속받을 추상화 클래스입니다.
    최초 작성일 : 2023.06.07
    업데이트 일자 :
    """
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y년 %m월 %d일 %R")
    
    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y년 %m월 %d일 %R")
    

class FundingSerializer(BaseSerializer):
    """
    작성자 : 최준영
    내용 : 펀딩 시리얼라이저 입니다.
    최초 작성일 : 2023.06.07
    업데이트 일자 : 
    """
    class Meta:
        model = Funding
        fields = "__all__"

    funding_startdate = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()

    def get_funding_startdate(self, obj):
        return obj.funding_startdate.strftime("%Y년 %m월 %d일 %R")
    
    def get_deadline(self, obj):
        return obj.deadline.strftime("%Y년 %m월 %d일 %R")


class FundingCreateSerializer(serializers.ModelSerializer):
    """
    작성자 : 최준영
    내용 : 펀딩 생성 시리얼라이저 입니다.
    최초 작성일 : 2023.06.07
    업데이트 일자 : 
    """
    class Meta:
        model = Funding
        fields = (
            "funding_startdate",
            "deadline",
            "goal",
            "current",
            "approvefile",
        )


class CampaignSerializer(BaseSerializer):
    """
    작성자 : 최준영
    내용 : 캠페인 시리얼라이저 입니다.
    obj.user.email를 name으로 나중에 변경하여 name값이 뜨도록 변경예정
    펀딩이 있는 캠페인이라면 "fundings"값이 정상적으로 뜨고,
    펀딩이 없는 캠페인이라면 "fundings"값이 null로 표기됩니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.07
    """
    class Meta:
        model = Campaign
        fields = (
            "id",
            "user",
            "like",
            "title",
            "content",
            "members",
            "current_members",
            "startdate",
            "enddate",
            "image",
            "status",
            "is_funding",
            "fundings",
        )

    user = serializers.SerializerMethodField()
    startdate = serializers.SerializerMethodField()
    enddate = serializers.SerializerMethodField()
    fundings = FundingSerializer()

    def get_user(self, obj):
        return obj.user.email
    
    def get_startdate(self, obj):
        return obj.startdate.strftime("%Y년 %m월 %d일 %R")
    
    def get_enddate(self, obj):
        return obj.enddate.strftime("%Y년 %m월 %d일 %R")
    

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


class CampaignReviewSerializer(BaseSerializer):
    """
    작성자 : 최준영
    내용 : 캠페인 리뷰 시리얼라이저 입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    class Meta:
        model = CampaignReview
        fields = "__all__"


class CampaignReviewCreateSerializer(serializers.ModelSerializer):
    """
    작성자 : 최준영
    내용 : 캠페인 리뷰 생성 시리얼라이저 입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    class Meta:
        model = CampaignReview
        fields = ("title", "content",)


class CampaignCommentSerializer(BaseSerializer):
    """
    작성자 : 최준영
    내용 : 캠페인 댓글 시리얼라이저 입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    class Meta:
        model = CampaignComment
        fields = "__all__"


class CampaignCommentCreateSerializer(serializers.ModelSerializer):
    """
    작성자 : 최준영
    내용 : 캠페인 댓글 생성 시리얼라이저 입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    class Meta:
        model = CampaignComment
        fields = ("content",)