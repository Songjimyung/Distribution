from django.urls import path
from campaigns import views

urlpatterns = [
    path('', views.CampaignView.as_view(), name='campaign_view'),
    path('create/', views.CampaignView.as_view(), name='campaign_view'),
    path('<int:campaign_id>/', views.CampaignDetailView.as_view(), name='campaign_detail_view'),
    path('review/<int:campaign_id>/', views.CampaignReviewView.as_view(), name='campaign_review_view'),
    path('review/<int:review_id>/', views.CampaignReviewDetailView.as_view(), name='campaign_review_detail_view'),
    path('comment/<int:campaign_id>/', views.CampaignCommentView.as_view(), name='campaign_comment_view'),
    path('comment/<int:comment_id>/', views.CampaignCommentDetailView.as_view(), name='campaign_comment_detail_view'),
    path('mypage/participart/', views.ParticipatingCampaignView.as_view(), name='participating_campaign'),
    path('mypage/review/', views.CampaignUserReviewView.as_view(), name='campaign_user_review'),
    path('mypage/like/', views.CampaignUserLikeView.as_view(), name='campaign_user_like'),
    path('mypage/comment/', views.CampaignUserCommentView.as_view(), name='campaign_comment'),
]