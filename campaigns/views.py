from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from campaigns.models import (
    Campaign, 
    CampaignComment, 
    CampaignReview, 
    Funding, 
    FundingOrder
)
from campaigns.serializers import (
    CampaignSerializer,
    CampaignCreateSerializer,
)


class CampaignView(APIView):
    """
    작성자 : 최준영
    내용 : 캠페인 뷰 입니다.
    전체 캠페인 리스트를 GET하는 get함수와
    캠페인을 작성할 수 있는 post함수입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        """
        캠페인의 진행 상태인 status가 2인 승인상태, 
        status가 3인 승인 + 완료 상태의 캠페인만 Q객체와 filter를 사용해
        비승인은 제외하고 Response하는 get함수입니다.
        """
        campaigns = Campaign.objects.filter(Q(status=2)|Q(status=3))
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Campaign Post 함수입니다.
        """
        serializer = CampaignCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CampaignDetailView(APIView):
    """
    작성자 : 최준영
    내용 : 캠페인 디테일 뷰 입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        pass

    def update(self, request):
        pass

    def delete(self, request):
        pass
