from django.urls import path

from .views import TransactionListAPIView, FundingTransactionView, WithdrawalTransactionView

urlpatterns = [
    path('', TransactionListAPIView.as_view(), name='loan-request-list'),
    path('fund-my-account/', FundingTransactionView.as_view(), name='fund-account'),
    path('withdraw-my-fund/', WithdrawalTransactionView.as_view(), name='withdraw-fund'),
    # path('<slug:slug>/details/', LoanRequestDetailAPIView.as_view(), name='loan-request-detail'),
]
