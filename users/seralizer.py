from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users import models


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserProfile
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'name',
            'gender',
            'age',
            'contact_no',
            'role'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_name(self, obj):
        return obj.name

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = models.UserProfile(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])

        user = models.UserProfile.objects.get(id=refresh['user_id'])

        access_token = refresh.access_token
        access_token['username'] = user.username
        access_token['email'] = user.email
        access_token['firstName'] = user.first_name
        access_token['lastName'] = user.last_name
        access_token['name'] = f"{user.first_name} {user.last_name}"
        access_token['gender'] = user.gender
        access_token['age'] = user.age
        access_token['contactNo'] = user.contact_no
        access_token['role'] = user.role

        data['access'] = str(access_token)
        return data
