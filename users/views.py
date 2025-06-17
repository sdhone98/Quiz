from rest_framework import generics
from resources import response_builder
from users.seralizer import UserRegistrationSerializer
from rest_framework import status
from users import helper

class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def get(self, request, *args, **kwargs):
        return response_builder(result=helper.get_all_users(), status_code=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return response_builder(result="User created successfully", status_code=status.HTTP_201_CREATED)
        return response_builder(result=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


