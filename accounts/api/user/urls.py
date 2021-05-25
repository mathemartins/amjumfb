from django.urls import path

from .views import UserDetailView, ProfileDetailView

urlpatterns = [
    path('', UserDetailView.as_view(), name='user-detail'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
]
