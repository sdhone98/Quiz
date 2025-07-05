from django.urls import path
from exam import views

urlpatterns = [
    path('attempt/start', views.quiz_start_details_fill, name='quiz_start_details_fill'),
    path('quiz-set', views.get_quiz_set, name='get_quiz_set'),
]
