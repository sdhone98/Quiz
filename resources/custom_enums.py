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


class QuestionType(Enum):
    OP_A = "A"
    OP_B = "B"
    OP_C = "C"
    OP_D = "D"

    @classmethod
    def choices(cls):
        return [(key.name.lower(), key.value) for key in cls]


class QuestionDifficultyType(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

    @classmethod
    def choices(cls):
        return [(key.name.lower(), key.value) for key in cls]
