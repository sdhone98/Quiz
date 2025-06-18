from rest_framework import status
from quiz.models import Topic, Question, Quiz, QuizSet
from resources import QuizExceptionHandler
from quiz.seralizer import (
    TopicSerializer,
    QuestionSerializer,
    QuizSerializer,
    QuizSetSerializer,
    QuizSetDetailsSerializer
)


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


def get_all_quizzes():
    quizzes = Quiz.objects.all()
    serialize = QuizSerializer(quizzes, many=True)
    return serialize.data


def add_quiz(validated_data):
    serializer = QuizSerializer(data=validated_data)

    if not serializer.is_valid():
        raise QuizExceptionHandler(
            error_msg=serializer.errors,
            error_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    serializer.save()


def update_quiz(quiz_id, validated_data):
    if quiz_id == 0:
        raise QuizExceptionHandler(
            error_msg="Please select a quiz Id",
            error_code=status.HTTP_406_NOT_ACCEPTABLE,
        )

    found_quiz = Quiz.objects.filter(id=quiz_id)

    if not found_quiz:
        raise QuizExceptionHandler(
            error_msg="Quiz not found",
            error_code=status.HTTP_404_NOT_FOUND,
        )
    found_quiz = found_quiz.first()

    # UPDATE QUIZ DETAILS
    found_quiz.title = validated_data.get("title", found_quiz.title)
    found_quiz.description = validated_data.get("description", found_quiz.description)
    found_quiz.is_active = validated_data.get("is_active", found_quiz.is_active)
    found_quiz.time_limit = validated_data.get("time_limit", found_quiz.time_limit)
    found_quiz.score = validated_data.get("score", found_quiz.score)

    found_quiz.save()


def delete_quiz(quiz_id):
    if quiz_id == 0:
        raise QuizExceptionHandler(
            error_msg="Please select a quiz Id",
            error_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    found_quiz = Quiz.objects.filter(id=quiz_id).first()

    if not found_quiz:
        raise QuizExceptionHandler(
            error_msg="Quiz not found",
            error_code=status.HTTP_404_NOT_FOUND,
        )

    found_quiz.delete()


def get_all_quiz_sets(q_set_id):
    quiz_sets = QuizSet.objects.filter(id=q_set_id) if q_set_id else QuizSet.objects.all()
    serialize = QuizSetSerializer(quiz_sets, many=True)
    return serialize.data


def get_all_quiz_sets_in_detail(q_set_id):
    quiz_sets = QuizSet.objects.filter(id=q_set_id) if q_set_id else QuizSet.objects.all()
    serialize = QuizSetDetailsSerializer(quiz_sets, many=True)
    return serialize.data


def add_quiz_set(validated_data):
    serializer = QuizSetSerializer(data=validated_data)
    if not serializer.is_valid():
        raise QuizExceptionHandler(
            error_msg=serializer.errors,
            error_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    serializer.save()


def update_quiz_set(quiz_id, validated_data):
    found_quiz_set = QuizSet.objects.get(id=quiz_id)
    new_q_list = validated_data.get("questions", None)
    if not found_quiz_set:
        raise QuizExceptionHandler(
            error_msg="Quiz not found",
            error_code=status.HTTP_404_NOT_FOUND,
        )

    if new_q_list is not None:
        old_q_list = list(
            found_quiz_set.questions.values_list('id', flat=True).all()
        )
        to_add = set(new_q_list) - set(old_q_list)
        to_removed = set(old_q_list) - set(new_q_list)
        if to_add:
            found_quiz_set.questions.add(*to_add)
        if to_removed:
            found_quiz_set.questions.remove(*to_removed)

    found_quiz_set.save()


def delete_quiz_set(quiz_set_id):
    if quiz_set_id == 0:
        raise QuizExceptionHandler(
            error_msg="Please select a quiz set",
            error_code=status.HTTP_406_NOT_ACCEPTABLE,
        )

    found_q_set = QuizSet.objects.filter(id=quiz_set_id).first()

    if not found_q_set:
        raise QuizExceptionHandler(
            error_msg="Quiz set not found",
            error_code=status.HTTP_404_NOT_FOUND,
        )

    found_q_set.delete()