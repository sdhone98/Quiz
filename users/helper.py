from django.contrib.auth.models import User
from users.seralizer import UserRegistrationSerializer


def get_all_users():
    found_user = User.objects.all()
    serializer = UserRegistrationSerializer(found_user, many=True)
    return serializer.data
