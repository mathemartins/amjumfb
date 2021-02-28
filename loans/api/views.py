from rest_framework import response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import Profile
from borrowers.models import Borrower
from loans.api.serializers import LoanRequestSerializer
from loans.models import LoanRequests


class LoanRequestListAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    serializer_class = LoanRequestSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 15

    def get_queryset(self):
        user_profile_obj = Profile.objects.get(user=self.request.user)
        borrower_obj = Borrower.objects.get(user=user_profile_obj)
        if borrower_obj.loanrequests_set.all().count() >= 1:
            return borrower_obj.loanrequests_set.all()
        response_data = {
            'request_status': 'Completed',
            'message': 'Loan Requests fetched successfully',
            'data': [{}]
        }
        return response_data


class LoanRequestDetailAPIView(RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    serializer_class = LoanRequestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        user_profile_obj = Profile.objects.get(user=self.request.user)
        borrower_obj = Borrower.objects.get(user=user_profile_obj)
        return borrower_obj.loanrequests_set.all()

    def get_object(self):
        slug = self.kwargs["slug"]
        return get_object_or_404(LoanRequests, slug=slug)
