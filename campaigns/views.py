from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
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
    CampaignReviewSerializer,
    CampaignReviewCreateSerializer,
    CampaignCommentSerializer,
    CampaignCommentCreateSerializer,
    FundingSerializer,
    FundingCreateSerializer,
)


class CampaignView(APIView):
    """
    작성자 : 최준영
    내용 : 캠페인 뷰 입니다.
    전체 캠페인 리스트를 GET하는 get함수와
    캠페인을 작성할 수 있는 post가 있는 클래스입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.08
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        """
        캠페인의 진행 상태인 status가 1 이상의 캠페인만 필터로 받아
        비승인은 제외하고 GET 요청에 대해 Response합니다.
        select_related를 사용해 eager-loading쪽으로 잡아봤습니다. (변경가능성높음)
        """
        queryset = Campaign.objects.filter(status__gte=1).select_related("fundings")
        serializer = CampaignSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        캠페인 POST요청 함수입니다.
        is_funding이 True라면 펀딩정보를 같이 POST하는 방식으로 모듈화 했습니다.
        """
        if request.data["is_funding"] == "False":
            return self.create_campaign(request)
        else:
            return self.create_campaign_with_funding(request)

    def create_campaign_with_funding(self, request):
        campaign_serializer = CampaignCreateSerializer(data=request.data)
        funding_serializer = FundingCreateSerializer(data=request.data)
        
        if campaign_serializer.is_valid() and funding_serializer.is_valid():
            campaign = campaign_serializer.save(user=request.user)
            funding_serializer.validated_data['campaign'] = campaign
            funding_serializer.save()
            response_data = {
                "message": "캠페인이 작성되었습니다.",
                "data": [campaign_serializer.data, funding_serializer.data]
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "캠페인 및 펀딩 정보가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

    def create_campaign(self, request):
        serializer = CampaignCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        response_data = {
            "message": "캠페인이 작성되었습니다.",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class CampaignDetailView(APIView):
    """
    작성자 : 최준영
    내용 : 캠페인 디테일 뷰 입니다.
    개별 캠페인 GET과 그 캠페인에 대한 PUT, DELETE 요청을 처리합니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 2023.06.07
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, campaign_id):
        """
        campaing_id를 Parameter로 받아 해당하는 캠페인에 GET 요청을 보내는 함수입니다.
        """
        # campaign = Campaign.objects.get(id=campaign_id)
        queryset = get_object_or_404(Campaign, id=campaign_id)
        serializer = CampaignSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, campaign_id):
        """
        campaing_id를 Parameter로 받아 해당하는 캠페인을 수정할 수 있는
        PUT 요청 함수입니다.
        is_funding이 True라면 펀딩정보를 같이 PUT하는 방식으로 모듈화 했습니다.
        """
        if request.data["is_funding"] == "False":
            return self.update_campaign(request, campaign_id)
        else:
            return self.update_campaign_with_funding(request, campaign_id)
        
    def update_campaign(self, request, campaign_id):
        queryset = get_object_or_404(Campaign, id=campaign_id)
        if request.user == queryset.user:
            serializer = CampaignCreateSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "캠페인 수정완료", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"캠페인 수정에 실패했습니다.", "errors": serializer.erros}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"해당 캠페인을 수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    def update_campaign_with_funding(self, request, campaign_id):
        queryset = get_object_or_404(Campaign, id=campaign_id)
        if request.user == queryset.user:
            campaign_serializer = CampaignCreateSerializer(queryset, data=request.data)
            funding_serializer = FundingCreateSerializer(data=request.data)
            if campaign_serializer.is_valid() and funding_serializer.is_valid():
                campaign = campaign_serializer.save()
                funding_serializer.validated_data['campaign'] = campaign
                funding_serializer.save()
                response_data = {
                    "message": "캠페인이 작성되었습니다.",
                    "data": [campaign_serializer.data, funding_serializer.data]
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "캠페인 및 펀딩 정보가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"해당 캠페인을 수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, campaign_id):
        """
        campaing_id를 Parameter로 받아 해당하는 캠페인을 삭제할 수 있는
        DELETE 요청 함수입니다.
        """
        queryset = get_object_or_404(Campaign, id=campaign_id)
        if request.user == queryset.user:
            queryset.delete()
            return Response({"message":"캠페인이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"해당 캠페인을 삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class CampaignReviewView(APIView):
    """
    작성자 : 최준영
    내용 : 캠페인 리뷰 뷰 입니다.
    완료가 된 캠페인의 리뷰에 대한 GET, POST 요청을 처리합니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    def get(self, request, campaign_id):
        """
        캠페인 리뷰를 볼 수 있는 GET 요청 함수입니다.
        """
        queryset = get_object_or_404(Campaign, id=campaign_id)
        review = queryset.reviews.all()
        serializer = CampaignReviewSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, campaign_id):
        """
        캠페인 리뷰를 작성하는 Post 요청 함수입니다.
        """
        serializer = CampaignReviewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, campaign_id=campaign_id)
        return Response({"message": "리뷰가 작성되었습니다.", "data": serializer.data}, status=status.HTTP_201_CREATED)


class CampaignReviewDetailView(APIView):
    """
    작성자 : 최준영
    내용 : 캠페인 리뷰 디테일 뷰 입니다.
    완료가 된 캠페인의 리뷰에 대한 PUT, DELETE 요청을 처리합니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    def put(self, request, review_id):
        """
        리뷰를 수정할 수 있는 PUT 요청 함수입니다.
        """
        queryset = get_object_or_404(CampaignReview, id=review_id)
        if request.user == queryset.user:
            serializer = CampaignReviewCreateSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "리뷰 수정완료", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"리뷰 수정에 실패했습니다.", "errors": serializer.erros}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"해당 리뷰를 수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, review_id):
        """
        리뷰를 삭제할 수 있는 DELETE 요청 함수입니다.
        """
        queryset = get_object_or_404(CampaignReview, id=review_id)
        if request.user == queryset.user:
            queryset.delete()
            return Response({"message":"리뷰가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"해당 리뷰를 삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class CampaignCommentView(APIView):
    """
    작성자 : 최준영
    내용 : 캠페인 댓글 뷰 입니다.
    캠페인의 댓글에 대한 GET, POST 요청을 처리합니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    def get(self, request, campaign_id):
        """
        캠페인 댓글을 볼 수 있는 GET 요청 함수입니다.
        """
        queryset = get_object_or_404(Campaign, id=campaign_id)
        comment = queryset.comments.all()
        serializer = CampaignCommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, campaign_id):
        """
        캠페인 댓글을 작성하는 Post 요청 함수입니다.
        """
        serializer = CampaignCommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, campaign_id=campaign_id)
        return Response({"message": "댓글이 작성되었습니다.", "data": serializer.data}, status=status.HTTP_201_CREATED)


class CampaignCommentDetailView(APIView):
    """
    작성자 : 최준영
    내용 : 캠페인 댓글 디테일 뷰 입니다.
    캠페인의 댓글에 대한 PUT, DELETE 요청을 처리합니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    def put(self, request, comment_id):
        """
        댓글을 수정할 수 있는 PUT 요청 함수입니다.
        """
        queryset = get_object_or_404(CampaignComment, id=comment_id)
        if request.user == queryset.user:
            serializer = CampaignCommentCreateSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "댓글 수정완료", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"댓글 수정에 실패했습니다.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"해당 댓글을 수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, comment_id):
        """
        댓글을 삭제할 수 있는 DELETE 요청 함수입니다.
        """
        queryset = get_object_or_404(CampaignComment, id=comment_id)
        if request.user == queryset.user:
            queryset.delete()
            return Response({"message":"댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"해당 댓글을 삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

def check_campaign_status():
    """
    작성자 : 최준영
    내용 : 캠페인 status 체크 함수입니다.
    status가 2인 캠페인 중 완료 날짜가 되거나 지난 캠페인의 status를
    3으로 바꿔주는 함수입니다.
    timezone.now()는 UTC기준 시각으로 찍히고,
    timezone.localtime()은 로컬 시각(한국)으로 찍히는데, 뭘 사용해야 할지는
    settings.py 시각과 MySQL에 찍히는 DB 시간 고려해서 정해야할 것 같습니다.
    최초 작성일 : 2023.06.08
    업데이트 일자 : 2023.06.08
    """
    now = timezone.now() # UTC로찍힘
    # now = timezone.localtime() # 한국 로컬타임 찍힘
    print(now)
    campaigns = Campaign.objects.filter(Q(status=2)|Q(status=3))

    for campaign in campaigns:
        if campaign.enddate <= now:
            campaign.status = 4
            campaign.save()
