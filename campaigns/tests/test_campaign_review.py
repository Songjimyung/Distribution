import random
import tempfile
from PIL import Image
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from users.models import User
from campaigns.models import Campaign, CampaignReview


def arbitrary_image(temp_text):
    """
    작성자 : 최준영
    내용 : 테스트용 임의 이미지 생성 함수입니다.
    최초 작성일 : 2023.06.09
    업데이트 일자 :
    """
    size = (50, 50)
    image = Image.new("RGBA", size)
    image.save(temp_text, "png")
    return temp_text


class CampaignReviewCreateReadTest(APITestCase):
    """
    작성자 : 최준영
    내용 : 캠페인 리뷰 GET, POST 요청 테스트 클래스입니다.
    최초 작성일 : 2023.06.09
    업데이트 일자 :
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "email": "test@test.com",
            "username": "John",
            "password": "Qwerasdf1234!",
        }
        date = timezone.now() + timedelta(seconds=random.randint(0, 86400))
        cls.campaign_data = {
            "title": "탄소발자국 캠페인 모집",
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
        temp_img = tempfile.NamedTemporaryFile()
        temp_img.name = "image.png"
        image_file = arbitrary_image(temp_img)
        image_file.seek(0)
        cls.campaign_data["image"] = image_file.name

        cls.user = User.objects.create_user(**cls.user_data)

        cls.campaign_data['user'] = User.objects.get(id=1)
        cls.campaign = Campaign.objects.create(**cls.campaign_data)
        cls.review_data = {
            "title": "탄소발자국 캠페인 모집 후기",
            "content": "보람찼다"
        }

    def setUp(self):
        self.access_token = self.client.post(reverse("log_in"), self.user_data).data[
            "access"
        ]

    def test_create_campaign_review(self):
        """
        캠페인 리뷰 POST 요청 테스트함수입니다.
        """
        url = reverse("campaign_review_view", kwargs={"campaign_id": self.campaign.id})
        response = self.client.post(
            path=url,
            data=self.review_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_read_campaign_review(self):
        """
        캠페인 리뷰 GET 요청 테스트함수입니다.
        """
        url = reverse("campaign_review_view", kwargs={"campaign_id": self.campaign.id})
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)


class CampaignReviewUpdateDeleteTest(APITestCase):
    """
    작성자 : 최준영
    내용 : 캠페인 리뷰 UPDATE, DELETE 요청 테스트 클래스입니다.
    최초 작성일 : 2023.06.09
    업데이트 일자 :
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "email": "test@test.com",
            "username": "John",
            "password": "Qwerasdf1234!",
        }
        date = timezone.now() + timedelta(seconds=random.randint(0, 86400))
        cls.campaign_data = {
            "title": "탄소발자국 캠페인 모집",
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
        temp_img = tempfile.NamedTemporaryFile()
        temp_img.name = "image.png"
        image_file = arbitrary_image(temp_img)
        image_file.seek(0)
        cls.campaign_data["image"] = image_file.name

        cls.user = User.objects.create_user(**cls.user_data)

        cls.campaign_data['user'] = User.objects.get(id=1)
        cls.campaign = Campaign.objects.create(**cls.campaign_data)

        cls.review_data = {
            "title": "탄소발자국 캠페인 모집 후기",
            "content": "보람찼다"
        }
        cls.new_review_data = {
            "title": "탄소발자국 캠페인 모집 후기",
            "content": "오늘도 채식 캠페인과 함께했는데, \
                작고 사소한 일이지만 탄소배출 감소에 이바지했다고 생각하니 뿌듯했습니다."
        }
        cls.review_data['user'] = User.objects.get(id=1)
        cls.review_data['campaign'] = Campaign.objects.get(id=1)
        cls.review = CampaignReview.objects.create(**cls.review_data)

    def setUp(self):
        self.access_token = self.client.post(reverse("log_in"), self.user_data).data[
            "access"
        ]

    def test_update_campaign_review(self):
        """
        캠페인 리뷰 PUT 요청 테스트함수입니다.
        """
        review = CampaignReview.objects.get(title=self.review_data['title'])
        url = review.get_absolute_url()
        response = self.client.put(
            path=url,
            data=self.new_review_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_campaign_review(self):
        """
        캠페인 리뷰 DELETE 요청 테스트함수입니다.
        """
        review = CampaignReview.objects.get(title=self.review_data['title'])
        url = review.get_absolute_url()
        response = self.client.delete(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 204)
