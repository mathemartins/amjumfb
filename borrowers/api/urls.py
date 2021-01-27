from django.urls import path

from .views import BorrowerDetailView

urlpatterns = [
    path('', BorrowerDetailView.as_view(), name='borrower-detail'),
]
