from django.contrib.auth.models import User
from rest_framework import serializers, status
from exam.models import QuizAttempt
from quiz.models import QuizSet, Topic
from resources import (
    QuizExceptionHandler,
    QuestionDifficultyType
)
from resources.custom_enums import QuizSetType


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

class GetQuizSetSerializer(serializers.Serializer):
    topic = serializers.IntegerField(required=True, help_text="Topic Id expected")
    difficulty = serializers.CharField(required=True, help_text="Difficulty type expected")
    set_type = serializers.CharField(required=True, help_text="Topic set expected")


    def validate(self, attrs):
        topic = attrs.get("topic")
        difficulty = attrs.get("difficulty")
        set_type = attrs.get("set_type")

        if not Topic.objects.filter(id=topic).exists():
            raise QuizExceptionHandler(
                error_msg=f"The topic '{topic}' does not exist.",
                error_code=status.HTTP_404_NOT_FOUND
            )

        if difficulty not in QuestionDifficultyType.all_values():
            raise QuizExceptionHandler(
                error_msg=f"The difficulty '{difficulty}' is not supported.",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )

        if set_type not in QuizSetType.all_values():
            raise QuizExceptionHandler(
                error_msg=f"The set type '{set_type}' is not supported.",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        return attrs


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = "__all__"


class QuizStartAttemptSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=True, help_text="User ID expected")
    quiz_set = serializers.IntegerField(required=True, help_text="Quiz ID expected")
    start_at = serializers.DateTimeField(required=True, help_text="Start time expected")

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
