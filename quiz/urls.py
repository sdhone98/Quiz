from django.contrib import admin
from django.urls import path, include
from quiz import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),

    path('api/quiz', views.TopicView.as_view(), name='topic'),
    path('api/question', views.QuestionView.as_view(), name='question'),

]
