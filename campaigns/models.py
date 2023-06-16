from django.db import models
from users.models import User
from django.urls import reverse


class BaseModel(models.Model):
    """
    작성자 : 최준영
    내용 : 베이스 모델입니다.
    중복되는 Field인 created_at과 updated_at을
    상속시킬 추상화 클래스입니다.
    최초 작성일 : 2023.06.07
    업데이트 일자 :
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Campaign(BaseModel):
    """
    작성자 : 최준영
    내용 : 캠페인에 대한 기본 모델입니다.
    is_funding의 BooleanField로 펀딩 여부를 체크하고
    status의 ChoiceField로 캠페인의 진행 상태를 체크합니다.
    status가 0일 때는 캠페인이 게시되지 않고, 1가 되었을 때 캠페인이 게시된 후,
    2이 되었을 때 캠페인의 모집이 시작됩니다.
    캠페인 활동기간이 시작되면 3으로 바뀌고, 정상 종료되었다면 4로 바뀝니다.
    status 5, 6, 7은 실패 여부에 따라 나누었습니다.
    글 게시 시, 활동이 없는 캠페인모금만 있다면 비워놔도 좋다고 써줘야할 것 같습니다
    is_funding이 False라면 Backoffice 검토 없이 그냥 게시해보는 것도 좋을 것 같아요

    캠페인 참여 유저 필드는 아직 미구현
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.08
    """

    class Meta:
        db_table = "campaign"

    STATUS_CHOICES = (
        (0, "미승인"),
        (1, "캠페인 예약중"),
        (2, "캠페인 모집중"),
        (3, "캠페인 활동중"),
        (4, "캠페인 종료"),
        (5, "캠페인 종료 - 펀딩 모금실패"),
        (6, "캠페인 종료 - 인원 모집실패"),
        (7, "캠페인 종료 - 모금/모집 실패"),
    )

    user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE, related_name="campaigns")
    participant = models.ManyToManyField(User, verbose_name="참가자", related_name="participants", blank=True)
    like = models.ManyToManyField(User, verbose_name="좋아요", related_name="likes", blank=True)
    title = models.CharField("제목", max_length=50)
    content = models.TextField("내용")
    members = models.PositiveIntegerField("모집 인원")
    campaign_start_date = models.DateTimeField("캠페인 시작일")
    campaign_end_date = models.DateTimeField("캠페인 마감일")
    activity_start_date = models.DateTimeField("활동 시작일", blank=True, null=True)
    activity_end_date = models.DateTimeField("활동 마감일", blank=True, null=True)
    image = models.ImageField("이미지", blank=True, null=True, upload_to="campaign/%Y/%m/")
    is_funding = models.BooleanField("펀딩여부", default=False)
    status = models.PositiveSmallIntegerField("진행 상태", choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("campaign_detail_view", kwargs={"campaign_id": self.id})


class CampaignReview(BaseModel):
    """
    작성자 : 최준영
    내용 : 캠페인 리뷰 모델입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.08
    """

    class Meta:
        db_table = "campaign_review"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField("캠페인 리뷰 제목", max_length=50)
    content = models.TextField("캠페인 리뷰 내용")

    def __str__(self):
        return str(self.title)
    
    def get_absolute_url(self):
        return reverse("campaign_review_detail_view", kwargs={"review_id": self.id})


class CampaignComment(BaseModel):
    """
    작성자 : 최준영
    내용 : 캠페인 댓글 모델입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.08
    """

    class Meta:
        db_table = "campaign_comment"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField("캠페인 댓글 내용")

    def __str__(self):
        return str(self.content)
    
    def get_absolute_url(self):
        return reverse("campaign_comment_detail_view", kwargs={"comment_id": self.id})


class Funding(BaseModel):
    """
    작성자 : 최준영
    내용 : 캠페인 펀딩 모델입니다.
    캠페인과의 관계는 OneToOne으로 변경하였습니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.07
    """

    class Meta:
        db_table = "funding"

    campaign = models.OneToOneField(
        Campaign, on_delete=models.CASCADE, related_name="fundings"
    )
    goal = models.PositiveIntegerField("펀딩 목표 금액")
    current = models.PositiveIntegerField("펀딩 현재 금액", default=0)
    approve_file = models.FileField("펀딩 승인 파일", upload_to="%Y/%m/", null=True, blank=True)

    def __str__(self):
        return str(self.goal)


class FundingOrder(BaseModel):
    """
    작성자 : 최준영
    내용 : 펀딩 결제정보 모델입니다.
    결제는 아직 import하지 않은 상황입니다.
    payment_text는 쓰일지 확정되지 않아 주석으로 처리해두겠습니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.08
    """

    class Meta:
        db_table = "funding_order"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fundingorders")
    funding = models.ForeignKey(Funding, on_delete=models.CASCADE, related_name="fundingorders")
    # payment_text = models.TextField("결제정보")
