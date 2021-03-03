from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import Profile
from borrowers.models import Borrower, BorrowerBankAccount


class BorrowerAccountDetails(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile_obj = Profile.objects.get(user=request.user)
            borrower_obj = Borrower.objects.get(user=user_profile_obj)
            borrower_amju_account = BorrowerBankAccount.objects.get(borrower=borrower_obj)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'Borrower Account fetched successfully',
                'data': [{
                    'account_number': borrower_amju_account.account_no,
                    'account_type': borrower_amju_account.get_account_type(),
                    'balance': borrower_amju_account.balance,
                }]
            }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'Borrower Account does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)


class BorrowerDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile_obj = Profile.objects.get(user=request.user)
            borrower_obj = Borrower.objects.get(user=user_profile_obj)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'Borrower profile fetched successfully',
                'data': [{
                    'address': borrower_obj.get_address(),
                    'lga': borrower_obj.lga,
                    'country': borrower_obj.country_text,
                    'businessName': borrower_obj.business_name,
                    'workingStatus': borrower_obj.working_status,
                    'nin': borrower_obj.unique_identifier,
                    'bank': borrower_obj.bank_text,
                    'accountNumber': borrower_obj.account_number,
                    'bvn': borrower_obj.bvn,
                    'age': borrower_obj.get_age()
                }]
            }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'Borrower profile does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)
