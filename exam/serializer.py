from django.contrib.auth.models import User
from rest_framework import serializers, status
from quiz.models import QuizSet
from resources import QuizExceptionHandler


class GetExamDataCheckSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=True, help_text="User ID expected")
    quiz_set = serializers.IntegerField(required=True, help_text="Quiz ID expected")

    def validate_user(self, user):
        if not User.objects.get(id=user).exists():
            raise QuizExceptionHandler(
                error_msg="User does not exist",
                error_code=status.HTTP_404_NOT_FOUND
        )
        return user

    def validate_quiz_set(self, quiz_set):
        if not QuizSet.objects.filter(id=quiz_set).exists():
            raise QuizExceptionHandler(
                error_msg="QuizSet does not exist",
                error_code=status.HTTP_404_NOT_FOUND
            )
        return quiz_set



