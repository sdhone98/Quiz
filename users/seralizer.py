from rest_framework import serializers
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
