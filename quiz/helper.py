from rest_framework import status
from quiz.models import Topic, Question
from quiz.seralizer import TopicSerializer, QuestionSerializer
from resources import QuizExceptionHandler


def get_all_topics():
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return serializer.data


def add_topic(validated_data):
    for topic_name in validated_data:
        serializer = TopicSerializer(data={"name": topic_name})
        if not serializer.is_valid():
            raise QuizExceptionHandler(
                error_msg=serializer.errors,
                error_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        serializer.save()


def update_topic(topic_name, topic_id):
    found_topic = Topic.objects.filter(id=topic_id).first()
    found_topic.name = topic_name.get("topic")
    found_topic.save()


def delete_topic(topic_id):
    found_topic = Topic.objects.filter(id=topic_id).first()

    if topic_id == 0:
        raise QuizExceptionHandler(
            error_msg="Please select a topic Id",
            error_code=status.HTTP_406_NOT_ACCEPTABLE,
        )

    if not found_topic:
        raise QuizExceptionHandler(
            error_msg="Topic not found",
            error_code=status.HTTP_404_NOT_FOUND,
        )

    found_topic.delete()


def get_all_questions():
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return serializer.data


def add_question(validated_data):
    serializer = QuestionSerializer(data=validated_data)
    if not serializer.is_valid():
        raise QuizExceptionHandler(
            error_msg=serializer.errors,
            error_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    serializer.save()


def delete_question(question_id):
    if question_id == 0:
        raise QuizExceptionHandler(
            error_msg="Please select a question Id",
            error_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    found_question = Question.objects.filter(id=question_id).first()

    if not found_question:
        raise QuizExceptionHandler(
            error_msg="Question not found",
            error_code=status.HTTP_404_NOT_FOUND,
        )
    found_question.delete()
