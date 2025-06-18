from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from quiz import (
    helper,
    seralizer
)
from resources import (
    response_builder,
    QuizExceptionHandler
)


class TopicView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            return response_builder(
                result=helper.get_all_topics(),
                status_code=status.HTTP_200_OK
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            return response_builder(
                result=e.message,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            validated_data = seralizer.TopicAddCheckSerializer(data=request.data)
            if not validated_data.is_valid():
                return response_builder(
                    result=validated_data.error_messages,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE
                )

            helper.add_topic(validated_data.data['topics'])

            return response_builder(
                result="Topic added successfully",
                status_code=status.HTTP_200_OK
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            return response_builder(
                result=e.message,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        try:
            topic_id = request.query_params.get("id", 0)
            validated_data = seralizer.TopicUpdateCheckSerializer(
                data=request.data,
                context={"topic_id": topic_id}
            )

            if not validated_data.is_valid():
                return response_builder(
                    result=validated_data.error_messages,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE
                )

            helper.update_topic(validated_data.data, topic_id)
            return response_builder(
                result="Topic updated successfully",
                status_code=status.HTTP_200_OK
            )

        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            return response_builder(
                result=e.message,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        try:
            topic_id = request.query_params.get("id", 0)

            helper.delete_topic(topic_id)

            return response_builder(
                result="Topic deleted successfully",
                status_code=status.HTTP_200_OK
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            return response_builder(
                result=e.message,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QuestionView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            return response_builder(
                result=helper.get_all_questions(),
                status_code=status.HTTP_200_OK
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            return response_builder(
                result=e.message,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            validated_data = seralizer.QuestionSerializer(data=request.data)

            if not validated_data.is_valid():
                return response_builder(
                    result=validated_data.errors,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE
                )

            helper.add_question(validated_data.data)

            return response_builder(
                result="Question added successfully",
                status_code=status.HTTP_200_OK
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            return response_builder(
                result=e.message,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        try:
            question_id = request.query_params.get("id", 0)
            helper.delete_question(question_id)

            return response_builder(
                result="Question deleted successfully",
                status_code=status.HTTP_200_OK
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            return response_builder(
                result=e.message,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
