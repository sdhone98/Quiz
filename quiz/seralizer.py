from rest_framework import serializers, status
from resources import QuizExceptionHandler, QuestionDifficultyType
from exam import models as exam_models
from quiz.models import (
    Topic,
    Question,
    QuizSet,
    QuizSetType,
)
from resources.custom_enums import (
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
        if not attrs.get("correct_option", None) in QuestionType.all_values():
            raise QuizExceptionHandler(
                error_msg=f"The question options '{attrs.get('correct_option')}' is not correct.",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )

        # VALIDATE DIFFICULTY LEVEL
        if not attrs.get("difficulty_level", None) in QuestionDifficultyType.all_values():
            raise QuizExceptionHandler(
                error_msg=f"The question '{attrs.get('difficulty_level')}' is not correct.",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        return attrs


class QuestionDetailsSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    question_text = serializers.SerializerMethodField()
    options_list = serializers.SerializerMethodField()
    correct_option = serializers.SerializerMethodField()
    difficulty_level = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.id

    def get_question_text(self, obj):
        return obj.question_text

    def get_options_list(self, obj):
        options = ["A", "B", "C", "D"]
        temp = []
        for op in options:
            field_name = f"option_{op.lower()}"
            value = getattr(obj, field_name, None)
            temp.append({"op_key": op, "op_value": value})
        return temp

    def get_correct_option(self, obj):
        return obj.correct_option

    def get_difficulty_level(self, obj):
        return obj.difficulty_level

    def get_topic(self, obj):
        return obj.topic.id


class QuizSetSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(),
        many=True
    )

    class Meta:
        model = QuizSet
        fields = '__all__'

    def validate(self, attrs):
        topic = attrs.get("topic")
        difficulty_level_key = attrs.get("difficulty_level")

        # CHECK TOPIC ID IS CORRECT
        if not isinstance(topic, Topic):
            raise QuizExceptionHandler(
                error_msg=f"The topic '{topic}' is not a topic.",
                error_code=status.HTTP_404_NOT_FOUND
            )

        if difficulty_level_key not in QuestionDifficultyType.all_values():
            raise QuizExceptionHandler(
                error_msg=f"Invalid difficulty level '{difficulty_level_key}', expected values: {QuestionDifficultyType.choices()}",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )

        if attrs["set_type"] not in QuizSetType.all_values():
            raise QuizExceptionHandler(
                error_msg=f"Invalid set type '{attrs['set_type']}', expected: {QuizSetType.choices()}",
                error_code=status.HTTP_406_NOT_ACCEPTABLE
            )

        for q in attrs["questions"]:
            if q.topic != topic:
                raise QuizExceptionHandler(
                    error_msg=f"Question '{q.question_text}' does not belong to Topic '{topic.name}'",
                    error_code=status.HTTP_406_NOT_ACCEPTABLE
                )
            if q.difficulty_level != attrs["difficulty_level"]:
                raise QuizExceptionHandler(
                    error_msg=f"Difficulty mismatch for Question '{q.question_text}'",
                    error_code=status.HTTP_406_NOT_ACCEPTABLE
                )
        return attrs


class QuizSetDetailsSerializer(serializers.Serializer):
    quiz_set_id = serializers.SerializerMethodField()
    topic_id = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    difficulty_level = serializers.SerializerMethodField()
    set_type = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()
    total_time = serializers.SerializerMethodField()

    def get_quiz_set_id(self, obj):
        return obj.id

    def get_topic_id(self, obj):
        return obj.topic.id

    def get_topic_name(self, obj):
        return obj.topic.name

    def get_is_completed(self, obj):
        return exam_models.QuizAttempt.objects.filter(
            user_id=self.context.get("user"),
            quiz_set__id=obj.id
        ).exists()

    def get_difficulty_level(self, obj):
        return obj.difficulty_level

    def get_set_type(self, obj):
        return obj.set_type

    def get_questions_count(self, obj):
        return obj.questions.count()

    def get_total_time(self, obj):
        return obj.total_time

    def get_questions(self, obj):
        return [
            {
                "id": q.id,
                "question_text": q.question_text,
                "options": {
                    "option_a": q.option_a,
                    "option_b": q.option_b,
                    "option_c": q.option_c,
                    "option_d": q.option_d,
                },

                "option_count": 4
            }
            for q in obj.questions.all()
        ]
