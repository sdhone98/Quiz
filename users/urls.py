from django.urls import path
from users import views

urlpatterns = [
    path('', views.UserView.as_view(), name='user-view'),
    path('<int:id>/', views.UserView.as_view(), name='user-detail-delete'),
    path('login', views.LoginView.as_view(), name='login'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
]
