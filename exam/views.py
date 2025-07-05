from rest_framework import status
from rest_framework.decorators import api_view
from resources import (
    response_builder,
    QuizExceptionHandler
)
from exam import (
    helper,
    serializer
)


@api_view(["POST"])
def get_quiz_set(request):
    try:
        validated_data = serializer.GetQuizSetSerializer(data=request.data)
        print(validated_data)
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


@api_view(['POST'])
def quiz_start_details_fill(request):
    try:
        validated_data = serializer.QuizAttemptSerializer(data=request.data)
        if not validated_data.is_valid():
            return response_builder(
                result=validated_data.errors,
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )
        user = int(validated_data.validated_data.get("user"))
        quiz_set = int(validated_data.validated_data.get("quiz_set"))
        start_at = int(validated_data.validated_data.get("start_at"))
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
