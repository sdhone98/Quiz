from django.db import models
from resources import (
    QuestionType,
    QuestionDifficultyType
)


class Topic(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "topic"
        managed = True


class Question(models.Model):
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200, default="N/A")
    option_d = models.CharField(max_length=200, default="N/A")
    correct_option = models.CharField(
        max_length=5,
        choices=QuestionType.choices()
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    difficulty_level = models.CharField(
        max_length=10,
        choices=QuestionDifficultyType.choices()
    )

    class Meta:
        db_table = "question"
        managed = True


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )
    difficulty_level = models.CharField(
        max_length=10,
        choices=QuestionDifficultyType.choices(),
        default=QuestionDifficultyType.EASY.value
    )
    is_active = models.BooleanField(default=False)
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes")
    score = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "quiz"
        managed = True


class QuizSet(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='sets'
    )
    questions = models.ManyToManyField(
        Question,
        related_name='in_quiz_sets'

    )

    class Meta:
        db_table = "quiz_set"
        managed = True
