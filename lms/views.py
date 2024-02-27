from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, CourseSubscribe
from lms.paginators import LMSPaginator
from lms.serializers import CourseSerializer, LessonSerializer, CourseSubscribeSerializer
from lms.permissions import IsModerator, IsOwner
from lms.tasks import send_course_update


# import requests
# from requests.exceptions import RequestException


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LMSPaginator

    def create(self, request, *args, **kwargs):
        is_moderator = request.user.groups.filter(name='moderator').exists()
        if is_moderator:
            return self.permission_denied(request)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        is_moderator = request.user.groups.filter(name='moderator').exists()
        if is_moderator:
            return self.permission_denied(request)

        return super().destroy(request, *args, **kwargs)


class CourseSubscribePostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()

    def post(self, request):
        user = self.request.user
        data = self.request.data
        course_id = data.get('course')
        course = get_object_or_404(Course, pk=course_id)
        sub_item = CourseSubscribe.objects.filter(user=user, course=course)
        print(sub_item)
        if not sub_item.exists:
            subscribe = CourseSubscribe.objects.create(user=user, course=course)
            message = 'Подписка на данный курс оформлена'
            subscribe.save()

        else:
            sub_item.delete()
            # sub_item.save()
            message = 'Подписка на данный курс удалена.'


        return Response({"message": message})


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]
    pagination_class = LMSPaginator


class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()
        if new_lesson:
            send_course_update.delay(new_lesson.course.id)


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsOwner | IsModerator]

    def perform_update(self, serializer):
        update_lesson = serializer.save()
        update_lesson.owner = self.request.user
        update_lesson.save()
        if update_lesson:
            send_course_update.delay(update_lesson.course.id)


class LessonDeleteView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsOwner | ~IsModerator]


class CourseSubscribeCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSubscribeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseSubscribeListAPIView(generics.ListAPIView):
    queryset = CourseSubscribe.objects.all()
    serializer_class = CourseSubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseSubscribe.objects.filter(user=self.request.user)


class CourseSubscribeDestroyAPIView(generics.DestroyAPIView):
    queryset = CourseSubscribe.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.user = self.request.user
        instance.delete()
