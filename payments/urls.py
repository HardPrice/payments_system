from django.urls import path
from . import views

urlpatterns = [
    path('webhook/bank/', views.BankWebhookView.as_view(), name='webhook-handler'),
    path('organizations/<str:inn>/balance/', views.OrganizationBalanceView.as_view(), name='organization-balance'),
]
