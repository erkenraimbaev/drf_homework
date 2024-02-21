from lms.models import Course, Lesson, CourseSubscribe
from rest_framework import serializers

from lms.validators import UrlFieldValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlFieldValidator(field='link_to_video')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lesson_set.all.count', read_only=True)
    lessons = LessonSerializer(source='lesson_set', read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        if user.is_authenticated:
            return CourseSubscribe.objects.filter(user=user, course=instance).exists()
        else:
            return False


class CourseSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscribe
        fields = '__all__'
