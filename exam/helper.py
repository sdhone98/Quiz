from rest_framework import status
from exam.models import QuizAttempt, UserAnswers
from exam.serializer import QuizResultDetailSerializer
from quiz import seralizer as quiz_serializer
from django.db.models import (
    Count,
    Subquery,
    OuterRef,
    IntegerField,
    Q,
    F,
    Value,
    Case,
    When,
    ExpressionWrapper,
    FloatField,
    CharField
)
from django.db.models.functions import (
    Concat,
    Cast
)
from resources import (
    QuizExceptionHandler,
    UserType
)
from quiz.models import (
    QuizSet,
    Topic
)
from exam import (
    serializer,
    models
)


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
    serializer_data = serializer.QuizAttemptSerializer(
        data={"user": user.id, "quiz_set": quiz_set.id, "start_at": start_at})
    if serializer_data.is_valid():
        quiz_attempt = serializer_data.save()
        response_data = serializer.QuizAttemptSerializer(quiz_attempt).data
        return response_data
    else:
        raise QuizExceptionHandler(
            error_msg=serializer_data.errors,
            error_code=status.HTTP_406_NOT_ACCEPTABLE
        )


def get_quiz_attempt_result_report(user, attempt):
    found_data = UserAnswers.objects.filter(
        attempt__id=attempt,
        attempt__user_id=user

    )

    questions_count = found_data[0].attempt.quiz_set.questions_count
    correct_answers = found_data.filter(is_correct=True).count()
    incorrect_answers = found_data.filter(is_correct=False).count()
    percentage = int(0.0 if questions_count == 0 else round((correct_answers / questions_count) * 100))

    return {
        "totalQuestions": questions_count,
        "correctAnswers": correct_answers,
        "incorrectAnswers": incorrect_answers,
        "percentage": percentage,
    }


def delete_user_quiz_attempt(user, quiz_set):
    found_user_attempt = QuizAttempt.objects.filter(
        user_id=user,
        quiz_set__id=quiz_set.id
    )
    if found_user_attempt:
        found_user_attempt_answers = UserAnswers.objects.filter(
            attempt__id=found_user_attempt[0].id
        )
        found_user_attempt_answers.delete()
    found_user_attempt.delete()
    return "User Quiz Attempt Deleted"


def get_quiz_result(user, user_role):
    if user_role == UserType.STUDENT.value:
        data = models.QuizAttempt.objects.filter(user_id=user, is_submitted=True)
        _serializer = QuizResultDetailSerializer(data, many=True)
        return _serializer.data
    if user_role == UserType.TEACHER.value:
        question_count_subquery = models.QuizSet.questions.through.objects.filter(
            quizset_id=OuterRef('pk')
        ).values('quizset_id').annotate(
            total_questions=Count('question_id')
        ).values('total_questions')[:1]

        # Fetch quiz sets created by the current user
        quiz_sets = models.QuizSet.objects.filter(
            user=user
        ).annotate(
            total_questions=Subquery(question_count_subquery, output_field=IntegerField())
        )

        results = []

        for quiz_set in quiz_sets:
            # Exclude quiz attempts by the quiz creator (self)
            submitted_attempts = models.QuizAttempt.objects.filter(
                quiz_set=quiz_set,
                is_submitted=True
            ).exclude(user=user)

            student_attempts = submitted_attempts.count()
            all_correct_students = 0

            for attempt in submitted_attempts:
                correct_count = models.UserAnswers.objects.filter(
                    attempt=attempt,
                    is_correct=True
                ).count()

                if correct_count == quiz_set.total_questions:
                    all_correct_students += 1

            not_all_correct_students = student_attempts - all_correct_students

            results.append({
                "quiz_set_id": quiz_set.id,
                "topic_name": quiz_set.topic.name,
                "difficulty_level": quiz_set.difficulty_level,
                "set_type": quiz_set.set_type,
                "student_attempts": student_attempts,
                "all_correct_students": all_correct_students,
                "not_all_correct_students": not_all_correct_students
            })
        return results
    return []


def get_leader_board_result(topic, difficulty):
    found_data = QuizAttempt.objects.filter(
        is_submitted=True
    )
    if topic:
        found_data = found_data.filter(
            quiz_set__topic__id=topic
        )
    if difficulty:
        found_data = found_data.filter(
            quiz_set__difficulty_level=difficulty
        )
    results = (
        found_data
        .annotate(
            quizSetId=F('quiz_set__id'),
            topicName=F('quiz_set__topic__name'),
            difficultyLevel=F('quiz_set__difficulty_level'),
            setType=F('quiz_set__set_type'),
            studentName=Concat(F('user__first_name'), Value(' '), F('user__last_name')),
            totalQuestions=Count('useranswers'),
            correctCount=Count('useranswers', filter=Q(useranswers__is_correct=True)),
            wrongCount=Count('useranswers', filter=Q(useranswers__is_correct=False)),
        )
        .annotate(
            percentage_int=Case(
                When(totalQuestions=0, then=Value(0)),
                default=ExpressionWrapper(
                    100 * F('correctCount') / F('totalQuestions'),
                    output_field=IntegerField()
                )
            )
        )
        .annotate(
            percentage=Concat(
                Cast('percentage_int', CharField()),
                Value('%')
            )
        )
        .values(
            'topicName',
            'difficultyLevel',
            'setType',
            'studentName',
            'totalQuestions',
            'correctCount',
            'wrongCount',
            'percentage',
        )
        .order_by('setType', 'correctCount', 'end_at')
    )
    return results


def get_leader_board_top_result(topic=None, difficulty=None):
    user_answers = UserAnswers.objects.all()

    if topic is not None:
        user_answers = user_answers.filter(question__topic_id=topic)
    if difficulty is not None:
        user_answers = user_answers.filter(question__difficulty=difficulty)

    top_users = (
        user_answers
        .values(
            user_id=F('attempt__user__id'),
            username=F('attempt__user__username'),
            first_name=F('attempt__user__first_name'),
            last_name=F('attempt__user__last_name')
        )
        .annotate(
            total_answers=Count('id'),
            correct_answers=Count('id', filter=Q(is_correct=True)),
            correct_percentage=ExpressionWrapper(
                100.0 * Count('id', filter=Q(is_correct=True)) / Count('id'),
                output_field=FloatField()
            )
        )
        .order_by('-correct_percentage')[:3]
    )
    response = []
    for position, user in enumerate(top_users, start=1):
        response.append({
            'position': position,
            'username': user['username'],
            'name': (user['first_name'] or '') + " " + (user['last_name'] or ''),
            'percentage': int(round(user['correct_percentage'], 1))
        })
    return response
