from users.models import User
from django.db import models
from quiz.models import QuizSet, Question
from resources import QuestionType


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    quiz_set = models.ForeignKey(QuizSet, on_delete=models.CASCADE)
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz_attempt'
        managed = True
        unique_together = ('user', 'quiz_set')


class UserAnswers(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, editable=False)
    submitted_ans = models.CharField(
        max_length=5,
        choices=QuestionType.choices()
    )

    class Meta:
        db_table = "user_answer"
        managed = True
        unique_together = ('attempt', 'question')

