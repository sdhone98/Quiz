from django.urls import path
from exam import views

urlpatterns = [
    path('quiz-set', views.get_quiz_set, name='get_quiz_set'),
    path('attempt/start', views.quiz_start_details_fill, name='quiz_start_details_fill'),
    path('attempt/submit', views.quiz_submit, name='quiz_submit'),
]
