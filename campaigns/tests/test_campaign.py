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