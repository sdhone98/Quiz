from django.contrib.auth.models import User
from rest_framework import status

from resources import QuizExceptionHandler
from users.seralizer import UserRegistrationSerializer


def get_all_users():
    found_user = User.objects.all()
    serializer = UserRegistrationSerializer(found_user, many=True)
    return serializer.data

def login(username, password):
    user = User.objects.filter(username=username).first()

    if not user:
        raise QuizExceptionHandler(
            error_msg=f"User with username '{username}' does not exist.",
            error_code=status.HTTP_404_NOT_FOUND,
        )

    # NOW CHECK THE PASSWORD
    if not user.check_password(password):

        raise QuizExceptionHandler(
            error_msg=f"Incorrect password. Please try again.",
            error_code=status.HTTP_406_NOT_ACCEPTABLE,
        )

    # LOGIN SUCCESSFUL
    serializer = UserRegistrationSerializer(user)

    return serializer.data
