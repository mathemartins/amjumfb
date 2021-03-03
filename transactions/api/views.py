from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import Profile
from borrowers.models import Borrower, BorrowerBankAccount
from company.models import Company
from transactions.api.serializers import TransactionSerializer
from transactions.models import Transaction


class TransactionListAPIView(ListAPIView):
    authentication_classes = [JSONWebTokenAuthentication, BasicAuthentication, SessionAuthentication]
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 15

    def get_queryset(self):
        user_profile_obj = Profile.objects.get(user=self.request.user)
        borrower_obj = Borrower.objects.get(user=user_profile_obj)
        print(borrower_obj)
        borrower_account = BorrowerBankAccount.objects.get(borrower=borrower_obj)
        return Transaction.objects.filter(account=borrower_account)


class FundingTransactionView(APIView):
    authentication_classes = [JSONWebTokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = request.data
        message = data.get('message')
        card_name = data.get('cardName')
        card_cvc = data.get('cardCVC')
        card_expiryMonth = data.get('expiryMonth')
        card_last4digits = data.get('last4Digits')
        card_number = data.get('cardNumber')
        card_type = data.get('cardType')
        reference = data.get('reference')
        status = data.get('status')
        method = data.get('method')
        verify = data.get('verify')

        company = "Amju"
        company_instance = Company.objects.get(name=company)
        user_profile_obj = Profile.objects.get(user=self.request.user)
        borrower_obj = Borrower.objects.get(user=user_profile_obj)
        borrower_account = BorrowerBankAccount.objects.get(borrower=borrower_obj)

        if message == 'Success':
            transact = Transaction.objects.create(
                company=company_instance,
                account=borrower_account,
                amount = 2000.00,
                transaction_type = 1,
            )
            print(transact)
            return Response({'detail': "Thank you for registering. Please verify your email."}, status=201)
        return Response({"detail": "Invalid Request"}, status=400)