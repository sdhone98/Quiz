from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
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
            is_flat = request.query_params.get("flat", False)
            is_flat = True if is_flat in ["true", "True", "t", "T"] else False
            return response_builder(
                result=helper.get_all_topics(is_flat),
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
                result=str(e),
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
                result=str(e),
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
                result=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(["GET"])
def get_topics_difficulty(request):
    try:
        return response_builder(
            result=helper.get_topics_difficulty(),
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

@api_view(["GET"])
def get_set_details(request):
    try:
        # validated_data = seralizer.SetCheckSerializer(data=request.data)
        # if not validated_data.is_valid():
        #     return response_builder(
        #         result=validated_data.error_messages,
        #         status_code=status.HTTP_406_NOT_ACCEPTABLE
        #     )

        return response_builder(
            result=helper.get_set_details(),
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
                result=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            is_bulk = isinstance(request.data, list)
            validated_data = seralizer.QuestionSerializer(data=request.data, many=is_bulk)

            if not validated_data.is_valid():
                return response_builder(
                    result=validated_data.errors,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE
                )

            validated_data.save()

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
                result=str(e),
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
                result=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QuizSetView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            in_detail = request.query_params.get("detail", False)
            q_set_id = request.query_params.get("id", False)
            difficulty_level = request.query_params.get("difficulty", False)
            if in_detail in ["True", "true", "TRUE", "T", "1"]:
                return response_builder(
                    result=helper.get_all_quiz_sets_in_detail(q_set_id, difficulty_level),
                    status_code=status.HTTP_200_OK
                )
            else:
                return response_builder(
                    result=helper.get_all_quiz_sets(q_set_id, difficulty_level),
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

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:
            serializer = seralizer.QuizSetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                return response_builder(
                    result="Quiz set created successfully",
                    status_code=status.HTTP_201_CREATED
                )
            return response_builder(
                result=serializer.errors,
                status_code=status.HTTP_406_NOT_ACCEPTABLE
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

    @transaction.atomic()
    def put(self, request, *args, **kwargs):
        try:
            quiz_set_id = request.query_params.get("id", 0)
            validated_data = seralizer.QuizSetSerializer(
                data=request.data,
                context={"quiz_set_id": quiz_set_id, "id_check": True},
            )
            if not validated_data.is_valid():
                return response_builder(
                    result=validated_data.errors,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE
                )
            helper.update_quiz_set(quiz_set_id, validated_data.data)

            return response_builder(
                result="Quiz set updated successfully",
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

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        try:
            quiz_set_id = request.query_params.get("id", 0)

            helper.delete_quiz_set(quiz_set_id)
            return response_builder(
                result="Quiz set deleted successfully",
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
