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
    CampaignReviewSerializer,
    CampaignReviewCreateSerializer,
    CampaignCommentSerializer,
    CampaignCommentCreateSerializer,
)


class CampaignView(APIView):
    """
    작성자 : 최준영
    내용 : 캠페인 뷰 입니다.
    전체 캠페인 리스트를 GET하는 get함수와
    캠페인을 작성할 수 있는 post가 있는 클래스입니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        """
        캠페인의 진행 상태인 status가 2인 승인상태, 
        status가 3인 승인 + 완료 상태의 캠페인만 Q객체와 filter를 사용해
        비승인은 제외하고 Response합니다.
        """
        campaigns = Campaign.objects.filter(Q(status=2)|Q(status=3))
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        캠페인을 작성하는 Post 요청 함수입니다.
        """
        serializer = CampaignCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"message": "캠페인이 작성되었습니다.", "data": serializer.data}, status=status.HTTP_201_CREATED)


class CampaignDetailView(APIView):
    """
    작성자 : 최준영
    내용 : 캠페인 디테일 뷰 입니다.
    개별 캠페인 GET과 그 캠페인에 대한 PUT, DELETE 요청을 처리합니다.
    최초 작성일 : 2023.06.06
    업데이트 일자 : 
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, campaign_id):
        """
        campaing_id를 파라미터로 받아 해당하는 캠페인을 볼 수 있는 GET 요청 함수입니다.
        """
        campaign = get_object_or_404(Campaign, id=campaign_id)
        serializer = CampaignSerializer(campaign)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, campaign_id):
        """
        campaing_id를 파라미터로 받아 해당하는 캠페인을 수정할 수 있는
        PUT 요청 함수입니다.
        """
        campaign = get_object_or_404(Campaign, id=campaign_id)
        if request.user == campaign.user:
            serializer = CampaignCreateSerializer(campaign, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "캠페인 수정완료", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"캠페인 수정에 실패했습니다.", "errors": serializer.erros}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"해당 캠페인을 수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, campaign_id):
        """
        campaing_id를 파라미터로 받아 해당하는 캠페인을 삭제할 수 있는
        DELTE 요청 함수입니다.
        """
        campaign = get_object_or_404(Campaign, id=campaign_id)
        if request.user == campaign.user:
            campaign.delete()
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
        campaign = get_object_or_404(Campaign, id=campaign_id)
        review = campaign.reviews.all()
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
        review = get_object_or_404(CampaignReview, id=review_id)
        if request.user == review.user:
            serializer = CampaignReviewCreateSerializer(review, data=request.data)
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
        review = get_object_or_404(CampaignReview, id=review_id)
        if request.user == review.user:
            review.delete()
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
        campaign = get_object_or_404(Campaign, id=campaign_id)
        comment = campaign.comments.all()
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
        comment = get_object_or_404(CampaignComment, id=comment_id)
        if request.user == comment.user:
            serializer = CampaignCommentCreateSerializer(comment, data=request.data)
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
        comment = get_object_or_404(CampaignComment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message":"댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"해당 댓글을 삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
