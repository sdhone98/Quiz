from rest_framework import status
from quiz.models import Topic, Question, QuizSet
from resources import QuizExceptionHandler
from resources.custom_enums import QuestionDifficultyType, QuestionType
from quiz.seralizer import (
    TopicSerializer,
    QuizSetSerializer,
    QuizSetDetailsSerializer,
    QuestionDetailsSerializer
)


def get_all_topics(is_flat):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    if is_flat:
        return [item['name'] for item in serializer.data]

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


def get_topics_difficulty():
    return [{"id": name, "name": name} for name in QuestionDifficultyType.all_values()]


def get_set_details():
    return [{"id": name, "name": name} for name in QuestionType.all_values()]


def get_all_questions(request):
    topic = request.query_params.get("topic", None)
    difficulty = request.query_params.get("difficulty", None)

    questions = Question.objects.all()

    if topic and difficulty:
        questions = Question.objects.filter(topic__id=int(topic), difficulty_level=difficulty)

    serializer = QuestionDetailsSerializer(questions, many=True)

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


def get_all_quiz_sets(q_set_id, difficulty_level, topic):
    quiz_sets = QuizSet.objects.filter(id=q_set_id) if q_set_id else QuizSet.objects.all()
    if difficulty_level:
        quiz_sets = quiz_sets.filter(difficulty_level__icontains=difficulty_level)
    if topic:
        quiz_sets = quiz_sets.filter(topic__id=topic)
    serialize = QuizSetSerializer(quiz_sets, many=True)
    return serialize.data


def get_all_quiz_sets_in_detail(q_set_id, difficulty_level, topic, user):
    quiz_sets = QuizSet.objects.filter(id=q_set_id) if q_set_id else QuizSet.objects.all()
    if difficulty_level:
        quiz_sets = quiz_sets.filter(difficulty_level__icontains=difficulty_level)
    if topic:
        quiz_sets = quiz_sets.filter(topic__id=topic)
    serialize = QuizSetDetailsSerializer(quiz_sets, many=True, context={"user": user})
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
