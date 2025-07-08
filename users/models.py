from django.db import models
from resources.custom_enums import GenderType, UserType
from django.contrib.auth.models import AbstractUser



class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GenderType.choices(), null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    contact_no = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=10, choices=UserType.choices(), default=UserType.default())
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    USERNAME_FIELD = 'username'


    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()
