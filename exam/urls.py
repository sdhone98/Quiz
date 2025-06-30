from django.urls import path
from exam import views

urlpatterns = [
    path('get-data', views.get_exam_data, name='get_exam_data'),
]
