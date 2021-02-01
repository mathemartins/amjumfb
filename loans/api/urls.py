from django.urls import path

from .views import LoanRequestListAPIView, LoanRequestDetailAPIView

urlpatterns = [
    path('', LoanRequestListAPIView.as_view(), name='loan-request-list'),
    path('<slug:slug>/details/', LoanRequestDetailAPIView.as_view(), name='loan-request-detail'),
]
