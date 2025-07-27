from rest_framework import status
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import TokenError
from quiz import settings
from resources import QuizExceptionHandler


def get_token_from_request(request):
    auth_header = request.headers.get("Authorization", None)
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return None


def decode_access_token(request):
    try:
        token = get_token_from_request(request)
        if not token:
            raise QuizExceptionHandler(
                error_msg="Token missing",
                error_code=status.HTTP_401_UNAUTHORIZED,
            )
        token_backend = TokenBackend(algorithm='HS256', signing_key=settings.SECRET_KEY)
        decoded_data = token_backend.decode(token, verify=True)
        return decoded_data
    except TokenError as e:
        return {"error": "Invalid token", "details": str(e)}
