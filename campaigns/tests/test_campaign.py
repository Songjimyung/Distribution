from django.urls import reverse
from rest_framework.test import APITestCase
from faker import Faker
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile
from users.models import User
from campaigns.models import (
    Campaign, 
    Funding, 
    FundingOrder
)
from campaigns.serializers import (
    CampaignSerializer,
    CampaignCreateSerializer,
)


class CampaignCreateTest(APITestCase):
    """
    작성자 : 최준영
    내용 : 캠페인 생성 테스트 클래스입니다.
    최초 작성일 : 2023.06.08
    업데이트 일자 : 
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "user_name": "leedddd",
            "email": "test@testuser.com",
            "password": "Qwerasdf1234!"
        }
        cls.movie_data = {
            "id": "397567",
            "title": "신과함께-죄와 벌",
            "release_date": "2017-12-20",
            "overview": "살인, 나태, 거짓, 불의, 배신, 폭력, 천륜 7개의 지옥에서 7번의 재판을 무사히 통과한 망자만이 환생하여\
                새로운 삶을 시작할 수 있다. 화재 사고 현장에서 여자아이를 구하고 죽음을 맞이한 소방관 자홍, 그의 앞에 저승차사\
                해원맥과 덕춘이 나타난다. 자신의 죽음이 아직 믿기지도 않는데 덕춘은 정의로운 망자이자 귀인이라며 그를 치켜세운다.",
            "vote_average": "7.9",
            "poster_path": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/5j2YVF7VouLG0Ze96SEsj4DnVQM.jpg",
            "genres": ["액션", "모험", "판타지", "스릴러"]
        }
    def setUp(self):
        self.access_token = self.client.post(reverse('user:token_obtain_pair'), self.user_data).data['access']



