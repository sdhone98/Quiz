from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, UserType


class UserDetailSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(source='userprofile.user_type')
    total_quizzes_taken = serializers.IntegerField(source='userprofile.total_quizzes_taken')
    average_score = serializers.FloatField(source='userprofile.average_score')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'total_quizzes_taken', 'average_score']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=UserType.choices(), default=UserType.default())
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'user_type', 'first_name', 'last_name', 'name']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # CREATE USER PROFILE
        UserProfile.objects.create(
            user=user,
            user_type=user_type
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
