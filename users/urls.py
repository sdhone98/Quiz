from django.urls import path
from users import views

urlpatterns = [
    path('', views.UserRegisterAPIView.as_view(), name='user-register'),
]