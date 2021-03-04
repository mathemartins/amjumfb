from dateutil.relativedelta import relativedelta
from django.utils import timezone
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
        amount = data.get('amount')
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

        amount = int(data.get('amount'))
        company = "Amju"
        company_instance = Company.objects.get(name=company)
        user_profile_obj = Profile.objects.get(user=self.request.user)
        borrower = Borrower.objects.get(user=user_profile_obj)
        borrower_account = BorrowerBankAccount.objects.get(borrower=borrower)

        if message == 'Success':
            if not borrower_account.initial_deposit_date:
                now = timezone.now()
                next_interest_month = int(12 / borrower_account.account_type.interest_calculation_per_year)
                borrower_account.initial_deposit_date = now
                borrower_account.interest_start_date = (
                        now + relativedelta(months=+next_interest_month)
                )
                borrower_account.company = company_instance
                borrower_account.borrower = borrower
                borrower_account.balance += amount
                borrower_account.save(
                    update_fields=[
                        'company',
                        'borrower',
                        'initial_deposit_date',
                        'balance',
                        'interest_start_date'
                    ]
                )
                borrower_account_new = BorrowerBankAccount.objects.get(borrower=borrower)
                Transaction.objects.create(
                    company=company_instance,
                    account=borrower_account,
                    amount=amount,
                    balance_after_transaction=borrower_account_new.balance,
                    transaction_type=1
                )
                payload_message = f'₦{amount} was deposited to your account successfully'
                return Response({'message': payload_message}, status=201)
            else:
                borrower_account.company = company_instance
                borrower_account.borrower = borrower
                borrower_account.balance += amount
                borrower_account.save(
                    update_fields=[
                        'company',
                        'borrower',
                        'balance',
                    ]
                )
                borrower_account_new = BorrowerBankAccount.objects.get(borrower=borrower)
                Transaction.objects.create(
                    company=company_instance,
                    account=borrower_account,
                    amount=amount,
                    balance_after_transaction=borrower_account_new.balance,
                    transaction_type=1
                )
                payload_message = f'₦{amount} was deposited to your account successfully'
                return Response({'message': payload_message})
        else:
            return Response({'message': "Payment Funding Was Unsuccesful, Try again!"})


class WithdrawalTransactionView(APIView):
    authentication_classes = [JSONWebTokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = request.data
        amount = int(data.get('amount'))
        company = "Amju"
        company_instance = Company.objects.get(name=company)
        user_profile_obj = Profile.objects.get(user=self.request.user)
        borrower = Borrower.objects.get(user=user_profile_obj)
        borrower_account = BorrowerBankAccount.objects.get(borrower=borrower)

        if borrower_account.balance >= amount:
            borrower_account.balance -= amount

            borrower_account.save(update_fields=['balance'])

            borrower_account_new = BorrowerBankAccount.objects.get(borrower=borrower)
            Transaction.objects.create(
                company=company_instance,
                account=borrower_account,
                amount=amount,
                balance_after_transaction=borrower_account_new.balance,
                transaction_type=2
            )

            payload_message = f'Successfully withdrawn ₦{amount} from your account'
            return Response({'message': payload_message}, status=201)
        else:
            payload_message = f'Request amount ₦{amount} cannot be withdrawn from your balance ₦{borrower_account.balance}'
            return Response({'message': payload_message}, status=400)