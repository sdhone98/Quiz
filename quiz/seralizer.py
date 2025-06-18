from rest_framework import serializers, status
from resources import QuizExceptionHandler
from quiz.models import (
    Topic,
    Question,
    Quiz,
    QuizSet,
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
        cleaned = []
        for topic in value:
            topic_clean = topic.strip().title()
            if Topic.objects.filter(name=topic_clean).exists():
                raise QuizExceptionHandler(
                    error_msg=f"The topic '{topic}' already exists.",
                    error_code=status.HTTP_226_IM_USED
                )

            cleaned.append(topic_clean)
        return cleaned


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


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSet
        fields = '__all__'

    def validate(self, attrs):
        # CHECK IF ID Exist OR NOT
        if self.context.get("id_check"):
            quiz_set_id = self.context.get("quiz_set_id")

            if not QuizSet.objects.filter(id=quiz_set_id).exists():
                raise QuizExceptionHandler(
                    error_msg=f"The quiz set '{quiz_set_id}' does not exist.",
                    error_code=status.HTTP_404_NOT_FOUND
                )
        quiz = attrs.get("quiz")
        questions = attrs.get("questions")

        for q in questions:
            if q.topic.id != quiz.topic.id:
                raise QuizExceptionHandler(
                    error_msg=f"'{q.question_text}' belongs to {quiz.topic.name} quiz, please choose correct one",
                    error_code=status.HTTP_406_NOT_ACCEPTABLE
                )
        return attrs


class QuizSetDetailsSerializer(serializers.ModelSerializer):
    quiz = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    class Meta:
        model = QuizSet
        fields = ['id', 'quiz', 'questions']

    def get_quiz(self, obj):
        return {
            "id": obj.quiz.id,
            "name": obj.quiz.title,
            "topic_id": obj.quiz.topic.id,
            "topic_name": obj.quiz.topic.name
        }

    def get_questions(self, obj):
        return [
            {
                "id": q.id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_option": q.correct_option,
                "topic": q.topic.id,
                "topic_name": q.topic.name,
                "difficulty_level": q.difficulty_level
            }
            for q in obj.questions.all()
        ]




