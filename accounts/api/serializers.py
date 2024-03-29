import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.settings import api_settings

from accounts.api.utils import expire_delta
from accounts.models import User, Profile
from borrowers.models import Borrower
from company.models import Company

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('User with email and password does not exists.')
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with given email and password does not exists')
        return {
            'email': user.email,
            'token': jwt_token
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'password',
            'password2',
            'token',
            'expires',

            'message',

        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        return "Thank you for registering. Please verify your email before continuing."

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def get_token(self, obj):  # instance of the model
        user = obj
        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_obj = User(email=validated_data.get('email'), full_name=validated_data.get('full_name'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.is_active = False
        user_obj.save()

        profile = Profile.objects.get(user=user_obj)
        full_name = str(validated_data.get('full_name'))
        first_name = full_name.split()[0]
        last_name = full_name.split()[1]
        company_instance = Company.objects.get(name='Amju')

        Borrower.objects.get_or_create(
            user=profile,
            first_name=first_name,
            last_name=last_name,
            email=validated_data.get('email'),
            registered_to=company_instance
        )

        return user_obj
