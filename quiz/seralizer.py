from rest_framework import serializers, status
from quiz.models import Topic, Question
from resources import QuizExceptionHandler

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