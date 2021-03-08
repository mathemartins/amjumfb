from django.utils.text import slugify
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import Profile
from amjuLoans import email_settings
from amjuLoans.utils import random_string_generator
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
        return borrower_obj.loanrequests_set.all()


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


class LoanRequestCreateAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = request.data
        user_profile_obj = Profile.objects.get(user=self.request.user)
        thisBorrower = Borrower.objects.get(user=user_profile_obj)

        message = data.get('message')
        amount = data.get('amount')

        LoanRequests.objects.create(
            borrower=thisBorrower,
            amount=amount,
            request_status='Still Processing',
            duration_figure=int(data.get('durationFigure')),
            duration=data.get('durationPeriod'),
            repayment_interval=data.get('repaymentInterval'),
            slug=slugify("{borrower}-{amount}-{primaryKey}".format(
                borrower=thisBorrower, amount=data.get('amount'), primaryKey=random_string_generator(6)
            ))
        )
        # Send an Email Saying Loan Application Was Made By A User
        html_ = "The User ({loanUser}), just applied for a loan, validate user account and process loan application".format(
            loanUser=thisBorrower)
        subject = 'New Loan Application From {loanUser}'.format(loanUser=thisBorrower)
        from_email = email_settings.EMAIL_HOST_USER
        recipient_list = ['amjuuniquemfb@gmail.com']

        from django.core.mail import EmailMessage
        message = EmailMessage(
            subject, html_, from_email, recipient_list
        )
        message.fail_silently = False
        message.send()
        return Response({'message': 'Loan Request Application Was Successful'}, status=201)
