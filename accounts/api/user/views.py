from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import Profile, User
from borrowers.models import Borrower


class UserDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile_obj = Profile.objects.get(user=request.user)
            borrower_obj = Borrower.objects.get(user=user_profile_obj)
            print(borrower_obj.get_age())
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'full_name': request.user.full_name,
                    'email': request.user.email,
                    'phone_number': user_profile_obj.get_phone(),
                    'image': user_profile_obj.get_image,
                    'age': borrower_obj.get_age(),
                    'gender': borrower_obj.gender,
                }]
            }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)
