from django.urls import path
from exam import views

urlpatterns = [
    path('quiz-set', views.get_quiz_set, name='get_quiz_set'),
    path('attempt/', views.QuizAttemptViewSet.as_view(), name='QuizAttemptViewSet'),
    path('attempt/submit', views.QuizResponseViewSet.as_view(), name='QuizResponseViewSet'),
    path('result', views.QuizResultViewSet.as_view(), name='QuizResultViewSet'),
]
