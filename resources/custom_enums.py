from enum import Enum

class UserType(Enum):
    ADMIN = "Admin"
    STUDENT = "Student"
    TEACHER = "Teacher"

    @classmethod
    def choices(cls):
        return [(key.name.lower(), key.value) for key in cls]

    @classmethod
    def default(cls):
        return cls.STUDENT.name.lower()