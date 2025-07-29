from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from exam.serializer import BulkUserAnswersSerializer
from resources import decode_access_token
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
@permission_classes([IsAuthenticated])
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
    permission_classes = [IsAuthenticated]
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

    def delete(self, request):
        try:
            _serializer = serializer.QuizAttemptDeleteSerializer(data=request.data)
            if not _serializer.is_valid():
                return response_builder(
                    result=_serializer.errors,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                )

            validated_data = _serializer.validated_data
            user = validated_data.get("user")
            quiz_set = validated_data.get("quiz_set")
            return response_builder(
                result=helper.delete_user_quiz_attempt(user, quiz_set),
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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
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

class QuizAttemptResultView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user_data = decode_access_token(request)
            user = user_data.get("user_id", False)
            attempt = request.query_params.get("attempt", False)

            if not attempt:
                response_builder(
                    result="Attempt not found",
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                )

            return response_builder(
                result=helper.get_quiz_attempt_result_report(user, attempt),
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



class QuizResultViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user_data = decode_access_token(request)
            user = user_data.get("user_id", False)
            user_role = user_data.get("role", False)
            return response_builder(
                result=helper.get_quiz_result(user, user_role),
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

class QuizResultLeaderBoardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            topic = request.query_params.get("topic", False)
            difficulty = request.query_params.get("difficulty", False)
            return response_builder(
                result=helper.get_leader_board_result(topic, difficulty),
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