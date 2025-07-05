from django.contrib.auth.models import User
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
    serializer = quiz_serializer.QuizSetDetailsSerializer(found_quiz_set, many=True)
    return serializer.data


def quiz_start_details_fill(username, quiz_set, start_at):
    user = User.objects.get(username=username)
    serializer_data = serializer.QuizAttemptSerializer({"user": user, "quiz_set": quiz_set, "start_at": start_at})

    if serializer_data.is_valid():
        serializer_data.save()
        return serializer_data
    else:
        raise QuizExceptionHandler(
            error_msg=serializer_data.errors,
            error_code=status.HTTP_406_NOT_ACCEPTABLE
        )
