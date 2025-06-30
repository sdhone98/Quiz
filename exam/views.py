from rest_framework import status
from rest_framework.decorators import api_view
from resources import response_builder, QuizExceptionHandler
from exam import (
    helper,
serializer
)


@api_view(['GET'])
def get_exam_data(request):
    try:
        data = {
            "user_id": request.query_params("user_id", 0),
            "quiz_set_id": request.query_params("quiz_set_id", 0),
        }
        validated_data = serializer.GetExamDataCheckSerializer(data=data)

        if not validated_data.is_valid():
            return response_builder(
                result=validated_data.errors,
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        return response_builder(
            result="Okay++",
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
