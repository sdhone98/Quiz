from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from resources import (
    response_builder,
    QuizExceptionHandler
)
from users.seralizer import (
    UserProfileSerializer,
    UserLoginSerializer,
    CustomTokenRefreshSerializer
)
from users import (
    helper,
    models
)


class UserView(APIView):
    def get(self, request, id=None):
        if id:
            user = get_object_or_404(models.UserProfile, id=id)
            serializer = UserProfileSerializer(user)
            return response_builder(
                result=serializer.data,
                status_code=status.HTTP_200_OK
            )
        else:
            users = models.UserProfile.objects.all()
            serializer = UserProfileSerializer(users, many=True)
            return response_builder(
                result=serializer.data,
                status_code=status.HTTP_200_OK
            )

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_builder(
                result=serializer.data,
                status_code=status.HTTP_200_OK
            )
        return response_builder(
            result=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id=None):
        if not id:
            return response_builder(
                result="User id is required",
                status_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        user = get_object_or_404(models.UserProfile, id=id)
        username = user.username
        user.delete()
        return response_builder(
            result=f"User '{username}' deleted successfully.",
            status_code=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if not serializer.is_valid():
                return response_builder(
                    result=serializer.error_messages,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE
                )

            username = serializer.validated_data.get('username', None)
            password = serializer.validated_data.get('password', None)

            return response_builder(
                result=helper.login(username, password),
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

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
