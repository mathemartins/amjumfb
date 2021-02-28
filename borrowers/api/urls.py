from django.urls import path

from .views import BorrowerDetailView, BorrowerAccountDetails

urlpatterns = [
    path('', BorrowerDetailView.as_view(), name='borrower-detail'),
    path('/account-details/', BorrowerAccountDetails.as_view(), name='borrower-account-detail'),
]