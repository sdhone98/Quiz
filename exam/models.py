from users.models import UserProfile
from django.db import models
from quiz.models import QuizSet, Question
from resources import QuestionType


class QuizAttempt(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, editable=False)
    quiz_set = models.ForeignKey(QuizSet, on_delete=models.CASCADE)
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz_attempt'
        managed = True
        unique_together = ('user', 'quiz_set')

    @property
    def quiz_completing_time(self):
        if self.end_at and self.start_at:
            delta = self.end_at - self.start_at
            total_seconds = int(delta.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes:02}:{seconds:02}"
        return "N/A"


class UserAnswers(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, editable=False)
    submitted_ans = models.CharField(
        max_length=5,
        choices=QuestionType.choices()
    )
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.question and self.submitted_ans:
            self.is_correct = self.submitted_ans == self.question.correct_option
        super(UserAnswers, self).save(*args, **kwargs)

    class Meta:
        db_table = "user_answer"
        managed = True
        unique_together = ('attempt', 'question')
