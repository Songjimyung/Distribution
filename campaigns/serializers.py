from rest_framework import serializers
from campaigns.models import (
    Campaign,
    CampaignReview,
    CampaignComment,
    Funding,
)


class BaseSerializer(serializers.ModelSerializer):
    """
    작성자 : 최준영
    내용 : 베이스 시리얼라이저입니다.
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


class FundingCreateSerializer(serializers.ModelSerializer):
    """
    작성자 : 최준영
    내용 : 펀딩 생성 시리얼라이저 입니다.
    최초 작성일 : 2023.06.07
    업데이트 일자 : 2023.06.20
    """

    class Meta:
        model = Funding
        fields = (
            "goal",
            "current",
            "approve_file",
        )


class CampaignSerializer(BaseSerializer):
    """
    작성자 : 최준영
    내용 : 캠페인 시리얼라이저 입니다.
    obj.user.email를 name으로 나중에 변경하여 name값이 뜨도록 변경 완료
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.18
    """

    class Meta:
        model = Campaign
        fields = (
            "id",
            "user",
            "like_count",
            "participant_count",
            "title",
            "content",
            "members",
            "campaign_start_date",
            "campaign_end_date",
            "activity_start_date",
            "activity_end_date",
            "image",
            "status",
            "is_funding",
            "created_at",
            "updated_at",
            "fundings",
        )

    user = serializers.SerializerMethodField()
    fundings = FundingSerializer()
    campaign_start_date = serializers.SerializerMethodField()
    campaign_end_date = serializers.SerializerMethodField()
    activity_start_date = serializers.SerializerMethodField()
    activity_end_date = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()


    def get_user(self, obj):
        return obj.user.username

    def get_campaign_start_date(self, obj):
        return obj.campaign_start_date.strftime("%Y년 %m월 %d일 %R")

    def get_campaign_end_date(self, obj):
        return obj.campaign_end_date.strftime("%Y년 %m월 %d일 %R")

    def get_activity_start_date(self, obj):
        if obj.activity_start_date:
            return obj.activity_start_date.strftime("%Y년 %m월 %d일 %R")
        else:
            pass

    def get_activity_end_date(self, obj):
        if obj.activity_end_date:
            return obj.activity_end_date.strftime("%Y년 %m월 %d일 %R")
        else:
            pass

    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_like_count(self, obj):
        return obj.like.count()

    def get_participant_count(self, obj):
        return obj.participant.count()


class CampaignCreateSerializer(serializers.ModelSerializer):
    """
    작성자 : 최준영
    내용 : 캠페인 생성 시리얼라이저 입니다.
    validation 진행중
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.20
    """

    class Meta:
        model = Campaign
        fields = (
            "title",
            "content",
            "members",
            "campaign_start_date",
            "campaign_end_date",
            "activity_start_date",
            "activity_end_date",
            "image",
            "is_funding",
            "status",
        )

    campaign_start_date = serializers.DateTimeField()
    campaign_end_date = serializers.DateTimeField()
    activity_start_date = serializers.DateTimeField(required=False, allow_null=True)
    activity_end_date = serializers.DateTimeField(required=False, allow_null=True)

    def validate(self, data):
        print(data)
        data = super().validate(data)
        data = self.validate_date(data)

        return data

    def validate_date(self, data):
        if data["campaign_start_date"] >= data["campaign_end_date"]:
            raise serializers.ValidationError(
                detail={"campaign_start_date": "캠페인 시작일은 마감일보다 이전일 수 없습니다."}
            )

        activity_start_date = data.get("activity_start_date")
        activity_end_date = data.get("activity_end_date")

        if activity_start_date and not activity_end_date:
            raise serializers.ValidationError(
                detail={"activity_end_date": "활동 종료일은 필수입니다."}
            )

        if not activity_start_date and activity_end_date:
            raise serializers.ValidationError(
                detail={"activity_start_date": "활동 시작일은 필수입니다."}
            )

        if activity_start_date and activity_end_date:
            if activity_start_date > activity_end_date:
                raise serializers.ValidationError(
                    detail={"activity_start_date": "활동 시작일은 마감일보다 이전일 수 없습니다."}
                )

        return data
    

class CampaignReviewSerializer(BaseSerializer):
    """
    작성자 : 최준영
    내용 : 캠페인 리뷰 시리얼라이저 입니다.
          +) author필드 추가 
    최초 작성일 : 2023.06.06
    업데이트 일자 :2023.06.16
    """

    class Meta:
        model = CampaignReview
        fields = "__all__"

    author = serializers.CharField(source="user.username", read_only=True)
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username


class CampaignReviewCreateSerializer(serializers.ModelSerializer):
    """
    작성자 : 최준영
    내용 : 캠페인 리뷰 생성 시리얼라이저 입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 :2023.06.16
    """

    class Meta:
        model = CampaignReview
        fields = (
            "title",
            "content",
            "image"
        )


class CampaignCommentSerializer(BaseSerializer):
    """
    작성자 : 최준영
    내용 : 캠페인 댓글 시리얼라이저 입니다.
          +) author필드 추가 
    최초 작성일 : 2023.06.06
    업데이트 일자 :2023.06.14
    """

    class Meta:
        model = CampaignComment
        fields = "__all__"

    author = serializers.CharField(source="user.username", read_only=True)
    campaign_title = serializers.CharField(
        source="campaign.title", read_only=True)
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username


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
