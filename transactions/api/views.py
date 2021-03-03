from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import Profile
from borrowers.models import Borrower, BorrowerBankAccount
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
        print(request.data, request.POST)
        # if request.user.is_authenticated():
        #     return Response({'detail': 'You are already registered and are authenticated.'}, status=400)
        # data = request.data
        # username = data.get('username')  # username or email address
        # email = data.get('username')
        # password = data.get('password')
        # password2 = data.get('password2')
        # qs = User.objects.filter(
        #     Q(username__iexact=username) |
        #     Q(email__iexact=username)
        # )
        # if password != password2:
        #     return Response({"password": "Password must match."}, status=401)
        # if qs.exists():
        #     return Response({"detail": "This user already exists"}, status=401)
        # else:
        #     user = User.objects.create(username=username, email=email)
        #     user.set_password(password)
        #     user.save()
        #     # payload = jwt_payload_handler(user)
        #     # token = jwt_encode_handler(payload)
        #     # response = jwt_response_payload_handler(token, user, request=request)
        #     # return Response(response, status=201)
        #     return Response({'detail': "Thank you for registering. Please verify your email."}, status=201)
        # return Response({"detail": "Invalid Request"}, status=400)
