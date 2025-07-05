from django.db import models
from resources import (
    QuestionType,
    QuestionDifficultyType
)
from resources.custom_enums import QuizSetType


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


class QuizSet(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="quiz_sets"
    )
    set_type = models.CharField(
        max_length=5,
        choices=QuizSetType.choices(),
        default=QuizSetType.SET_A.value
    )
    difficulty_level = models.CharField(
        max_length=10,
        choices=QuestionDifficultyType.choices(),
        default=QuestionDifficultyType.EASY.value
    )
    questions = models.ManyToManyField(
        Question,
        related_name='in_quiz_sets'

    )
    total_time = models.IntegerField(default=10)

    def save(self, *args, **kwargs):
        if "total_time" not in self or not self.total_time or self.total_time <= 0:
            match self.difficulty_level:
                case QuestionDifficultyType.EASY.value:
                    self.total_time = 10
                case QuestionDifficultyType.MEDIUM.value:
                    self.total_time = 15
                case QuestionDifficultyType.HARD.value:
                    self.total_time = 20
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.topic.name}-{self.set_type}-{self.difficulty_level}"

    class Meta:
        db_table = "quiz_set"
        managed = True
        unique_together = ("topic", "set_type", "difficulty_level")
