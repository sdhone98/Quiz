from rest_framework import serializers, status
from resources import QuizExceptionHandler, QuestionDifficultyType
from quiz.models import (
    Topic,
    Question,
    QuizSet,
)
from resources.custom_enums import (
    QuizSetType,
    QuestionType,
    QuestionDifficultyType
)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class TopicAddCheckSerializer(serializers.Serializer):
    topics = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )

    def validate_topics(self, value):
        for topic in value:
            topic_clean = topic.strip().lower()
            if Topic.objects.filter(name__iexact=topic_clean).exists():
                raise QuizExceptionHandler(
                    error_msg=f"The topic '{topic}' already exists.",
                    error_code=status.HTTP_226_IM_USED
                )
        return value


class TopicUpdateCheckSerializer(serializers.Serializer):
    topic = serializers.CharField(required=True)

    def validate_topic(self, topic):
        topic_clean = topic.strip().title()
        topic_id = self.context.get("topic_id")

        if not Topic.objects.filter(id=topic_id).exists():
            raise QuizExceptionHandler(
                error_msg=f"The topic '{topic}' does not exist.",
                error_code=status.HTTP_404_NOT_FOUND
            )

        if Topic.objects.filter(
                name=topic_clean
        ).exclude(
            id=topic_id
        ).exists():
            raise QuizExceptionHandler(
                error_msg=f"The topic '{topic}' already exists.",
                error_code=status.HTTP_226_IM_USED
            )
        return topic


class SetCheckSerializer(serializers.Serializer):
    topic = serializers.IntegerField(required=True)
    difficulty = serializers.CharField(required=True)

    def validate(self, attrs):
        topic = attrs.get("topic")
        difficulty = attrs.get("difficulty")
        if not Topic.objects.filter(id=topic).exists():
            raise QuizExceptionHandler(
                error_msg=f"The topic '{topic}' does not exist.",
                error_code=status.HTTP_404_NOT_FOUND
            )

        if difficulty not in QuestionDifficultyType.all_values():
            raise QuizExceptionHandler(
                error_msg=f"The difficulty '{difficulty}' is not supported.",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        return attrs


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def validate(self, attrs):
        # VALIDATE ANSWER OPTION
        if not attrs.get("correct_option", None) in QuestionType.all_keys():
            raise QuizExceptionHandler(
                error_msg=f"The question '{attrs.get('correct_option')}' is not correct.",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )

        attrs["correct_option"] = QuestionType[attrs.get("correct_option")].value

        # VALIDATE DIFFICULTY LEVEL
        if not attrs.get("difficulty_level", None) in QuestionDifficultyType.all_keys():
            raise QuizExceptionHandler(
                error_msg=f"The question '{attrs.get('difficulty_level')}' is not correct.",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        attrs["difficulty_level"] = QuestionDifficultyType[attrs.get("difficulty_level")].value
        return attrs


# class QuizSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Quiz
#         fields = '__all__'


class QuizSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSet
        fields = '__all__'

    def validate(self, attrs):
        # CHECK TOPIC ID IS CORRECT
        if not isinstance(attrs.get("topic", None), Topic):
            raise QuizExceptionHandler(
                error_msg=f"The topic '{attrs.get('topic')}' is not a topic.",
                error_code=status.HTTP_404_NOT_FOUND
            )

        # CHECK SET TYPE
        if not attrs.get("set_type", None) in QuizSetType.all_keys():
            raise QuizExceptionHandler(
                error_msg=f"Invalid set type'{attrs.get('set_type')}', expected set type is {QuizSetType.choices()}.",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        attrs["set_type"] = QuizSetType[attrs.get("set_type")].value

        # CHECK QUIZ SET DIFFICULTY LEVEL
        difficulty_level = attrs.get("difficulty_level")
        if not difficulty_level in QuestionDifficultyType.all_keys():
            raise QuizExceptionHandler(
                error_msg=f"Invalid difficulty level for Quiz '{attrs.get('difficulty_level')}', expected difficulty_level is {QuestionDifficultyType.choices()}.",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        attrs["difficulty_level"] = QuestionDifficultyType[attrs.get("difficulty_level")].value
        difficulty_level = attrs.get("difficulty_level")

        # VALIDATION QUESTIONS
        questions = attrs.get("questions", [])
        topic = attrs.get("topic")
        for q in questions:
            if q.topic.id != topic.id:
                raise QuizExceptionHandler(
                    error_msg=f"'{q.question_text}' belongs to {topic.name} quiz, please choose correct one",
                    error_code=status.HTTP_406_NOT_ACCEPTABLE
                )
            if difficulty_level != q.difficulty_level:
                raise QuizExceptionHandler(
                    error_msg=f"Please choose correct difficulty level Quiz Difficulty is {difficulty_level} and Question: {q.question_text} Difficulty is {q.difficulty_level}",
                    error_code=status.HTTP_406_NOT_ACCEPTABLE
                )
        return attrs


class QuizSetDetailsSerializer(serializers.Serializer):
    quiz_set_id = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()
    total_time = serializers.SerializerMethodField()

    def get_quiz_set_id(self, obj):
        return obj.id

    def get_questions_count(self, obj):
        return obj.questions.count()

    def get_total_time(self, obj):
        return obj.total_time

    def get_questions(self, obj):
        return [
            {
                "id": q.id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d
            }
            for q in obj.questions.all()
        ]
