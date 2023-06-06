from django.urls import path
from campaigns import views


urlpatterns = [
    path('list/', views.CampaignView.as_view(), name='campaign_view'),
    path('create/', views.CampaignView.as_view(), name='campaign_view'),
]
