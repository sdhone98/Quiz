from django.contrib import admin
from django.urls import path, include
from quiz import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/exam/', include('exam.urls')),

    path('api/topic', views.TopicView.as_view(), name='topic'),
    path('api/topic/difficulty', views.get_topics_difficulty, name='difficulty'),
    path('api/topic/difficulty/set', views.get_set_details, name='set_details'),
    path('api/question', views.QuestionView.as_view(), name='question'),
    path('api/quiz-set', views.QuizSetView.as_view(), name='quiz_set'),
    path('api/quiz-set-details', views.QuizSetDetailsView.as_view(), name='QuizSetDetailsView'),
]
