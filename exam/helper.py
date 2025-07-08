from rest_framework import status
from quiz.models import QuizSet, Topic
from quiz import seralizer as quiz_serializer
from resources import QuizExceptionHandler
from exam import serializer


def get_quiz_set(topic, difficulty, set_type):
    topic = Topic.objects.get(id=topic)
    found_quiz_set = QuizSet.objects.filter(topic__id=topic.id, difficulty_level=difficulty, set_type=set_type)
    if not found_quiz_set:
        raise QuizExceptionHandler(
            error_msg=f"No quiz set for this choice 'Topic:{topic.name}, difficulty:{difficulty}, Set:{set_type}'.",
            error_code=status.HTTP_404_NOT_FOUND
        )
    _serializer = quiz_serializer.QuizSetDetailsSerializer(found_quiz_set, many=True)
    data = _serializer.data[0] if _serializer.data else {}
    return data


def quiz_start_details_fill(user, quiz_set, start_at):
    serializer_data = serializer.QuizAttemptSerializer(data={"user": user.id, "quiz_set": quiz_set.id, "start_at": start_at})

    if serializer_data.is_valid():
        serializer_data.save()
    else:
        raise QuizExceptionHandler(
            error_msg=serializer_data.errors,
            error_code=status.HTTP_406_NOT_ACCEPTABLE
        )
