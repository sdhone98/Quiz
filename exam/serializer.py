from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.validators import UniqueTogetherValidator
from resources.custom_enums import QuizSetType
from users.models import UserProfile
from exam.models import (
    QuizAttempt,
    UserAnswers
)
from quiz.models import (
    QuizSet,
    Topic,
    Question
)
from resources import (
    QuizExceptionHandler,
    QuestionDifficultyType
)


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
        validators = [
            UniqueTogetherValidator
        ]

    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    quiz_set = serializers.PrimaryKeyRelatedField(queryset=QuizSet.objects.all())
    start_at = serializers.DateTimeField(
        input_formats=["%a, %d %b %Y %H:%M:%S %Z"]
    )

    def validate(self, attrs):
        user = attrs.get("user")
        quiz_set = attrs.get("quiz_set")
        user_name = self.initial_data.get("user_name")

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
                error_msg=f"The quiz '{quiz_set.topic.name} - {quiz_set.difficulty_level} - {quiz_set.set_type}' is already attempted by the user.",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )

        return attrs


class QuizAttemptDeleteSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    quiz_set = serializers.PrimaryKeyRelatedField(queryset=QuizSet.objects.all())


class UserAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswers
        fields = "__all__"


class UserAnswerSubmissionSerializer(serializers.Serializer):
    questionId = serializers.IntegerField()
    selectedOption = serializers.CharField()


class BulkUserAnswersSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    attempt = serializers.IntegerField()
    quiz_user_response = UserAnswerSubmissionSerializer(many=True)

    def validate(self, attrs):
        try:
            attrs["attempt_obj"] = QuizAttempt.objects.get(id=attrs["attempt"], user_id=attrs["user"])
        except QuizAttempt.DoesNotExist:
            raise serializers.ValidationError("Invalid user or attempt.")

        return attrs

    def create(self, validated_data):
        attempt = validated_data["attempt_obj"]
        responses = validated_data["quiz_user_response"]

        user_answers = []

        # MARK QUIZ COMPLETE IN QUIZ ATTEMPT
        QuizAttempt.objects.filter(
            id=attempt.id,
            user_id=attempt.user_id
        ).update(
            end_at=timezone.now(),
            is_submitted=True
        )

        for response in responses:
            question = Question.objects.get(id=response["questionId"])
            submitted_ans = response["selectedOption"]

            user_answer = UserAnswers(
                attempt=attempt,
                question=question,
                submitted_ans=submitted_ans
            )
            user_answer.save()
            user_answers.append(user_answer)

        return user_answers


class QuizResultDetailSerializer(serializers.Serializer):
    topic_id = serializers.IntegerField(source='quiz_set.topic.id')
    topic_name = serializers.CharField(source='quiz_set.topic.name')
    set_type = serializers.CharField(source='quiz_set.set_type')
    difficulty_level = serializers.CharField(source='quiz_set.difficulty_level')
    completed_time = serializers.SerializerMethodField()
    total_time = serializers.IntegerField(source='quiz_set.total_time')
    quiz_set = serializers.IntegerField(source='quiz_set.id')
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()
    total_questions = serializers.SerializerMethodField()
    correct_answers = serializers.SerializerMethodField()
    wrong_answers = serializers.SerializerMethodField()

    def get_completed_time(self, obj):
        return obj.quiz_completing_time

    def get_total_questions(self, obj):
        return UserAnswers.objects.filter(attempt=obj).count()

    def get_correct_answers(self, obj):
        return UserAnswers.objects.filter(attempt=obj, is_correct=True).count()

    def get_wrong_answers(self, obj):
        return UserAnswers.objects.filter(attempt=obj, is_correct=False).count()
