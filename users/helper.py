from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from resources import QuizExceptionHandler
from django.contrib.auth import get_user_model
User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

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

    return {
        'access': str(access_token),
        'refresh': str(refresh),
    }

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

    return get_tokens_for_user(user)
