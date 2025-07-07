from django.contrib.auth.models import User
from rest_framework import serializers, status
from exam.models import QuizAttempt
from quiz.models import QuizSet, Topic, Question
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

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    quiz_set = serializers.PrimaryKeyRelatedField(queryset=QuizSet.objects.all())
    start_at = serializers.DateTimeField()

    def validate(self, attrs):
        user = attrs.get("user")  # Already a User object now
        quiz_set = attrs.get("quiz_set")  # Already a QuizSet object now
        user_name = self.initial_data.get("user_name")  # still from raw input

        if not user:
            raise QuizExceptionHandler(
                error_msg=f"The user '{user_name}' does not exist.",
                error_code=status.HTTP_404_NOT_FOUND
            )

        if not quiz_set:
            raise QuizExceptionHandler(
                error_msg="The quiz set does not exist.",
                error_code=status.HTTP_404_NOT_FOUND
            )

        if QuizAttempt.objects.filter(quiz_set=quiz_set, user=user).exists():
            raise QuizExceptionHandler(
                error_msg=f"The quiz set '{quiz_set.topic.name} - {quiz_set.difficulty_level} - {quiz_set.set_type}' is already attempted by the user.",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )

        return attrs




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


class GetQuizSetCheckSerializer(serializers.Serializer):
    topic = serializers.IntegerField(required=True, help_text="Topic ID expected")
    difficulty = serializers.CharField(required=True, help_text="Difficulty type expected")

    def validate(self, attrs):
        topic = attrs.get("topic")
        difficulty = attrs.get("difficulty")

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

        return attrs
