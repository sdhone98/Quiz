from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from resources import UserType


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices(),
        default=UserType.STUDENT
    )
    total_quizzes_taken = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    last_active = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"
