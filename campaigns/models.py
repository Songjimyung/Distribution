from django.db import models
from users.models import User


class Campaign(models.Model):
    """
    작성자 : 최준영
    내용 : 캠페인에 대한 기본 모델입니다.
    is_funding의 BooleanField로 펀딩 여부를 체크하고
    status의 ChoiceField로 캠페인의 진행 상태를 체크합니다.
    status가 1일 때는 캠페인이 게시되지 않고, 2가 되었을 때 캠페인이 게시된 후, 
    3이 되었을 때 캠페인이 완료처리 됩니다.
    STATUS_CHOICES는 0시작이 좋을지, 1시작이 좋을지 고민됩니다
    is_funding이 False라면 Backoffice 검토 없이 그냥 게시해보는 것도 좋을 것 같아요
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    class Meta:
        db_table = "campaign"
    STATUS_CHOICES = (
        (1, "캠페인 미승인 상태"),
        (2, "캠페인 승인 상태"),
        (3, "캠페인 승인, 완료 상태"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="campaigns")
    like = models.ManyToManyField(User, related_name="likes", blank=True)
    title = models.CharField("캠페인 제목", max_length=50)
    content = models.TextField("캠페인 내용")
    members = models.PositiveIntegerField("캠페인 모집 인원")
    current_members = models.PositiveIntegerField("캠페인 현재 참가인원", default=0)
    startdate = models.DateTimeField("캠페인 시작일")
    enddate = models.DateTimeField("캠페인 마감일")
    created_at = models.DateTimeField("캠페인 작성일", auto_now_add=True)
    updated_at = models.DateTimeField("캠페인 수정일", auto_now=True)
    image = models.ImageField("캠페인 이미지", blank=True, upload_to="%Y/%m/")
    is_funding = models.BooleanField("캠페인 펀딩여부", default=False)
    status = models.PositiveSmallIntegerField("캠페인 진행 상태", choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return str(self.title)


class CampaignReview(models.Model):
    """
    작성자 : 최준영
    내용 : 캠페인 리뷰 모델입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    class Meta:
        db_table = "campaign review"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField("캠페인 리뷰 제목", max_length=50)
    content = models.TextField("캠페인 리뷰 내용")
    created_at = models.DateTimeField("캠페인 리뷰 작성일", auto_now_add=True)
    updated_at = models.DateTimeField("캠페인 리뷰 수정일", auto_now=True)

    def __str__(self):
        return str(self.title)


class CampaignComment(models.Model):
    """
    작성자 : 최준영
    내용 : 캠페인 댓글 모델입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    class Meta:
        db_table = "campaign comment"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField("캠페인 댓글 내용")
    created_at = models.DateTimeField("캠페인 댓글 작성일", auto_now_add=True)
    updated_at = models.DateTimeField("캠페인 댓글 수정일", auto_now=True)

    def __str__(self):
        return str(self.content)


class Funding(models.Model):
    """
    작성자 : 최준영
    내용 : 캠페인 펀딩 모델입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    class Meta:
        db_table = "funding"

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="fundings")
    funding_startdate = models.DateTimeField("펀딩 생성일", auto_now_add=True)
    deadline = models.DateTimeField("펀딩 마감일")
    goal = models.PositiveIntegerField("펀딩 목표 금액")
    current = models.PositiveIntegerField("펀딩 현재 금액", default=0)
    approvefile = models.FileField("펀딩 승인 파일", upload_to="%Y/%m/", blank=True)

    def __str__(self):
        return str(self.goal)
    

class FundingOrder(models.Model):
    """
    작성자 : 최준영
    내용 : 펀딩 결제정보 모델입니다.
    결제는 아직 import하지 않은 상황입니다.
    payment_text는 쓰일지 확정되지 않아 주석으로 처리해두겠습니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    class Meta:
        db_table = "funding order"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fundingorders")
    funding = models.ForeignKey(Funding, on_delete=models.CASCADE, related_name="fundingorders")
    # payment_text = models.TextField("결제정보")
