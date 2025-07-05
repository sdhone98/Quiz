from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import generics
from rest_framework.views import APIView
from resources import (
    response_builder,
    QuizExceptionHandler
)
from users.seralizer import UserRegistrationSerializer
from rest_framework import status
from users import (
    helper,
    seralizer
)


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def get(self, request, *args, **kwargs):
        return response_builder(result=helper.get_all_users(), status_code=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return response_builder(result="User created successfully", status_code=status.HTTP_201_CREATED)
        return response_builder(result=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        try:
            username = request.query_params.get("username", None)
            if not username:
                return response_builder(
                    result="User id is required",
                    status_code=status.HTTP_406_NOT_ACCEPTABLE
                )

            user = User.objects.filter(username=username)
            if not user:
                return response_builder(
                    result=f"User not found with username:'{username}'.!",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            user.delete()
            return response_builder(
                result=f'User {username} deleted successfully.',
                status_code=status.HTTP_200_OK
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )

        except Exception as e:
            return response_builder(
                result=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    def post(self, request):
        try:
            serializer = seralizer.UserLoginSerializer(data=request.data)
            if not serializer.is_valid():
                return response_builder(
                    result=serializer.error_messages,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE
                )

            username = serializer.validated_data.get('username', None)
            password = serializer.validated_data.get('password', None)

            user = authenticate(username=username, password=password)
            if not user:
                return response_builder(
                    result=f"User not found with username:'{username}'.!",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            serializer = UserRegistrationSerializer(user)
            return response_builder(
                result=serializer.data,
                status_code=status.HTTP_200_OK
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )

        except Exception as e:
            return response_builder(
                result=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
