from django.urls import path

from .views import LoanRequestListAPIView, LoanRequestDetailAPIView, LoanRequestCreateAPIView

urlpatterns = [
    path('', LoanRequestListAPIView.as_view(), name='loan-request-list'),
    path('create/', LoanRequestCreateAPIView.as_view(), name='loan-request-create'),
    path('<slug:slug>/details/', LoanRequestDetailAPIView.as_view(), name='loan-request-detail'),
]
