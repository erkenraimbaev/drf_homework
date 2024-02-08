from lms.models import Course, Lesson
from rest_framework import serializers


# Serializers define the API representation.
class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'preview', 'description', 'link_to_video']
