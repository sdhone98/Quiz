from django.urls import path
from exam import views

urlpatterns = [
    path('quiz-set', views.get_quiz_set, name='get_quiz_set'),
    path('attempt/', views.QuizAttemptViewSet.as_view(), name='QuizAttemptViewSet'),
    path('attempt/submit', views.QuizResponseViewSet.as_view(), name='QuizResponseViewSet'),
    path('attempt/result', views.QuizAttemptResultView.as_view(), name='QuizAttemptResultView'),
    path('result', views.QuizResultViewSet.as_view(), name='QuizResultViewSet'),
    path('leaderboard', views.QuizResultLeaderBoardView.as_view(), name='QuizResultLeaderBoardView'),
]
