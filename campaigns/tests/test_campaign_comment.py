import random
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from users.models import User
from campaigns.models import Campaign, CampaignComment


class CampaignCommentCreateReadTest(APITestCase):
    """
    작성자 : 최준영
    내용 : 캠페인 댓글 GET, POST 요청 테스트 클래스입니다.
    최초 작성일 : 2023.06.09
    업데이트 일자 :
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "email": "test@test.com",
            "name": "John",
            "password": "Qwerasdf1234!",
        }
        date = timezone.now() + timedelta(seconds=random.randint(0, 86400))
        cls.campaign_data = {
            "content": "탄소발자국 캠페인 모집",
            "content": "더 나은 세상을 위한 지구별 눈물 닦아주기, 이제 우리가 행동에 나설 때입니다.",
            "members": "200",
            "current_members": "0",
            "campaign_start_date": date,
            "campaign_end_date": date,
            "activity_start_date": date,
            "activity_end_date": date,
            "image": "",
            "is_funding": "False",
            "status": "1",
        }
        cls.user = User.objects.create_user("test@test.com", "John", "Qwerasdf1234!")
        cls.campaign_data['user'] = User.objects.get(id=1)
        cls.campaign = Campaign.objects.create(**cls.campaign_data)
        cls.comment_data = {
            "content": "좋은 캠페인이네요"
        }

    def setUp(self):
        self.access_token = self.client.post(reverse("log_in"), self.user_data).data[
            "access"
        ]

    def test_create_campaign_comment(self):
        """
        캠페인 댓글 POST 요청 테스트함수입니다.
        """
        url = reverse("campaign_comment_view", kwargs={"campaign_id": self.campaign.id})
        response = self.client.post(
            path=url,
            data=self.comment_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_read_campaign_comment(self):
        """
        캠페인 댓글 GET 요청 테스트함수입니다.
        """
        url = reverse("campaign_comment_view", kwargs={"campaign_id": self.campaign.id})
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)


class CampaignCommentUpdateDeleteTest(APITestCase):
    """
    작성자 : 최준영
    내용 : 캠페인 댓글 UPDATE, DELETE 요청 테스트 클래스입니다.
    최초 작성일 : 2023.06.09
    업데이트 일자 :
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "email": "test@test.com",
            "name": "John",
            "password": "Qwerasdf1234!",
        }
        date = timezone.now() + timedelta(seconds=random.randint(0, 86400))
        cls.campaign_data = {
            "content": "탄소발자국 캠페인 모집",
            "content": "더 나은 세상을 위한 지구별 눈물 닦아주기, 이제 우리가 행동에 나설 때입니다.",
            "members": "200",
            "current_members": "0",
            "campaign_start_date": date,
            "campaign_end_date": date,
            "activity_start_date": date,
            "activity_end_date": date,
            "image": "",
            "is_funding": "False",
            "status": "1",
        }
        cls.comment_data = {
            "content": "좋은 캠페인이네요"
        }
        cls.new_comment_data = {
            "content": "좋은 캠페인이네요. 꼭 참여하고 싶습니다!"
        }
        cls.user = User.objects.create_user("test@test.com", "John", "Qwerasdf1234!")

        cls.campaign_data['user'] = User.objects.get(id=1)
        cls.campaign = Campaign.objects.create(**cls.campaign_data)

        cls.comment_data['user'] = User.objects.get(id=1)
        cls.comment_data['campaign'] = Campaign.objects.get(id=1)
        cls.comment = CampaignComment.objects.create(**cls.comment_data)

    def setUp(self):
        self.access_token = self.client.post(reverse("log_in"), self.user_data).data[
            "access"
        ]

    def test_update_campaign_comment(self):
        """
        캠페인 댓글 PUT 요청 테스트함수입니다.
        """
        comment = CampaignComment.objects.get(content=self.comment_data['content'])
        url = comment.get_absolute_url()
        response = self.client.put(
            path=url,
            data=self.new_comment_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_campaign_comment(self):
        """
        캠페인 댓글 DELETE 요청 테스트함수입니다.
        """
        comment = CampaignComment.objects.get(content=self.comment_data['content'])
        url = comment.get_absolute_url()
        response = self.client.delete(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 204)
