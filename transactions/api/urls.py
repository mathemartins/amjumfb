from django.urls import path

from .views import TransactionListAPIView, FundingTransactionView

urlpatterns = [
    path('', TransactionListAPIView.as_view(), name='loan-request-list'),
    path('fund-my-account/', FundingTransactionView.as_view(), name='fund-account'),
    # path('<slug:slug>/details/', LoanRequestDetailAPIView.as_view(), name='loan-request-detail'),
]
