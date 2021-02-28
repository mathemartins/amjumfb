from django.urls import path

from .views import TransactionListAPIView

urlpatterns = [
    path('', TransactionListAPIView.as_view(), name='loan-request-list'),
    # path('<slug:slug>/details/', LoanRequestDetailAPIView.as_view(), name='loan-request-detail'),
]
