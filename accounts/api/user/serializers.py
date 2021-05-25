from rest_framework import serializers

from accounts.models import User, Profile


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password',)


class UserRegistrationSerializer(serializers.ModelSerializer):

    user_ = UserDetailSerializer(required=False)

    class Meta:
        model = User
        fields = ('user_',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data)
        return user
