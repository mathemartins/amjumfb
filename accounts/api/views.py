from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from accounts.api.permissions import AnonPermissionOnly
from accounts.api.serializers import UserLoginSerializer, UserRegisterSerializer
from accounts.api.user.serializers import UserRegistrationSerializer
from accounts.models import User


class UserLoginView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated'}, status=400)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token': serializer.data['token'],
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


# class UserRegistrationView(CreateAPIView):
#     serializer_class = UserRegistrationSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         status_code =status.HTTP_201_CREATED
#         response = {
#             'success': True,
#             'status_code': status_code,
#             'message': 'An Email Has Been Sent To You For Confirmation, Please Activate Your Account'
#         }
#         return Response(response, status=status_code)


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly,]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


# class RegisterAPIView(APIView):
#     permission_classes      = [permissions.AllowAny]
#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated():
#             return Response({'detail': 'You are already registered and are authenticated.'}, status=400)
#         data = request.data
#         username        = data.get('username') # username or email address
#         email           = data.get('username')
#         password        = data.get('password')
#         password2       = data.get('password2')
#         qs = User.objects.filter(
#                 Q(username__iexact=username)|
#                 Q(email__iexact=username)
#             )
#         if password != password2:
#             return Response({"password": "Password must match."}, status=401)
#         if qs.exists():
#             return Response({"detail": "This user already exists"}, status=401)
#         else:
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             # payload = jwt_payload_handler(user)
#             # token = jwt_encode_handler(payload)
#             # response = jwt_response_payload_handler(token, user, request=request)
#             # return Response(response, status=201)
#             return Response({'detail': "Thank you for registering. Please verify your email."}, status=201)
#         return Response({"detail": "Invalid Request"}, status=400)
