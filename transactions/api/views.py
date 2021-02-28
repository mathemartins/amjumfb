from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import Profile
from borrowers.models import Borrower, BorrowerBankAccount
from transactions.api.serializers import TransactionSerializer
from transactions.models import Transaction


class TransactionListAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 15

    def get_queryset(self):
        user_profile_obj = Profile.objects.get(user=self.request.user)
        borrower_obj = Borrower.objects.get(user=user_profile_obj)
        return BorrowerBankAccount.objects.get(borrower=borrower_obj).transactions
