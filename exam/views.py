from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from exam.serializer import BulkUserAnswersSerializer
from resources import (
    response_builder,
    QuizExceptionHandler
)
from exam import (
    helper,
    serializer,
    models
)


@api_view(["POST"])
def get_quiz_set(request):
    try:
        validated_data = serializer.GetQuizSetSerializer(data=request.data)
        if not validated_data.is_valid():
            return response_builder(
                result=validated_data.error_messages,
                status_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        topic = validated_data.data.get("topic")
        difficulty = validated_data.data.get("difficulty")
        set_type = validated_data.data.get("set_type")
        return response_builder(
            result=helper.get_quiz_set(topic, difficulty, set_type),
            status_code=status.HTTP_200_OK
        )
    except QuizExceptionHandler as e:
        return response_builder(
            result=e.error_msg,
            status_code=e.error_code
        )
    except Exception as e:
        return response_builder(
            result=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class QuizAttemptViewSet(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # models.QuizAttempt.objects.all().delete()
            user = request.query_params.get("user", False)
            quiz_set = request.query_params.get("quiz_set", False)
            if user and quiz_set:
                data = models.QuizAttempt.objects.filter(
                    user=user,
                    quiz_set__id=quiz_set
                ).values().first()
            else:
                data = models.QuizAttempt.objects.all().values()
            return response_builder(
                result=data,
                status_code=status.HTTP_200_OK,
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            return response_builder(
                result=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            _serializer = serializer.QuizAttemptSerializer(data=request.data)
            if not _serializer.is_valid():
                return response_builder(
                    result=_serializer.errors,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                )
            validated_data = _serializer.validated_data
            user = validated_data.get("user")
            quiz_set = validated_data.get("quiz_set")
            start_at = validated_data.get("start_at")
            return response_builder(
                result=helper.quiz_start_details_fill(user, quiz_set, start_at),
                status_code=status.HTTP_200_OK
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            return response_builder(
                result=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QuizResponseViewSet(APIView):
    def get(self, request):
        try:
            # models.UserAnswers.objects.all().delete()
            data = models.UserAnswers.objects.all().values()

            return response_builder(
                result=data,
                status_code=status.HTTP_200_OK
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            return response_builder(
                result=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def post(self, request):
        try:
            _serializer = BulkUserAnswersSerializer(data=request.data)
            if _serializer.is_valid():
                _serializer.save()
                return response_builder(
                    result="saved quiz answers",
                    status_code=status.HTTP_200_OK,
                )
            else:
                return response_builder(
                    result=_serializer.errors,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            return response_builder(
                result=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuizResultViewSet(APIView):
    def get(self, request):
        try:
            user = request.query_params.get("user", False)
            return response_builder(
                result=helper.get_quiz_result(user),
                status_code=status.HTTP_200_OK
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            return response_builder(
                result=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)