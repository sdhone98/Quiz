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


class QuizView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            return response_builder(
                result=helper.get_all_quizzes(),
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
            validated_data = seralizer.QuizSerializer(data=request.data)
            if not validated_data.is_valid():
                return response_builder(
                    result=validated_data.errors,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE
                )
            helper.add_quiz(validated_data.data)

            return response_builder(
                result="Quiz created successfully",
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
    def put(self, request, *args, **kwargs):
        try:
            quiz_id = request.query_params.get("id", 0)
            validated_data = seralizer.QuizSerializer(data=request.data)
            if not validated_data.is_valid():
                return response_builder(
                    result=validated_data.errors,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE
                )

            helper.update_quiz(quiz_id, validated_data.data)
            return response_builder(
                result="Quiz updated successfully",
                status_code=status.HTTP_200_OK
            )
        except QuizExceptionHandler as e:
            return response_builder(
                result=e.error_msg,
                status_code=e.error_code
            )
        except Exception as e:
            print(e)
            return response_builder(
                result=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        try:
            quiz_id = request.query_params.get("id", 0)

            helper.delete_quiz(quiz_id)
            return response_builder(
                result="Quiz deleted successfully",
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

            if in_detail:
                return response_builder(
                    result=helper.get_all_quiz_sets_in_detail(q_set_id),
                    status_code=status.HTTP_200_OK
                )
            else:
                return response_builder(
                    result=helper.get_all_quiz_sets(q_set_id),
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
            validated_data = seralizer.QuizSetSerializer(data=request.data)
            if not validated_data.is_valid():
                return response_builder(
                    result=validated_data.errors,
                    status_code=status.HTTP_406_NOT_ACCEPTABLE
                )
            helper.add_quiz_set(validated_data.data)

            return response_builder(
                result="Quiz set created successfully",
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
