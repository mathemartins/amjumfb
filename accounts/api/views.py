from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from accounts.api.serializers import UserLoginSerializer


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

# class AuthAPIView(APIView):
#     permission_classes = [AnonPermissionOnly]
#
#     def post(self, request, *args, **kwargs):
#         print(request.user)
#         if request.user.is_authenticated:
#             return Response({'detail': 'You are already authenticated'}, status=400)
#         data = request.data
#         email = data.get('email')  # username or email address
#         password = data.get('password')
#         qs = User.objects.filter(Q(email__iexact=email)).distinct()
#         if qs.count() == 1:
#             user_obj = qs.first()
#             if user_obj.check_password(password):
#                 user = authenticate(email=email, password=password)
#                 payload = jwt_payload_handler(user)
#                 token = jwt_encode_handler(payload)
#                 response = jwt_response_payload_handler(token, user, request=request)
#                 return Response(response)
#         return Response({"detail": "Invalid credentials"}, status=401)


# class RegisterAPIView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegisterSerializer
#     permission_classes = [AnonPermissionOnly]
#
#     def get_serializer_context(self, *args, **kwargs):
#         return {"request": self.request}


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
