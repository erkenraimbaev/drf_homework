from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, CourseSubscribe
from lms.paginators import LMSPaginator
from lms.serializers import CourseSerializer, LessonSerializer, CourseSubscribeSerializer
from lms.permissions import IsModerator, IsOwner
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

    def post(self, request, course_id):
        user = request.user
        course = get_object_or_404(Course, id=course_id)
        sub, created_sub = CourseSubscribe.objects.get_or_create(user=user, course=course)
        if created_sub:
            message = 'Подписка на данный курс оформлена'
            created_sub.save()
        elif sub:
            sub.delete()
            sub.save()
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


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsOwner | IsModerator]


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

# class SomeAPIView(APIView):
#
#     def get(self, *args, **kwargs):
#         try:
#             response = requests.get('https://api.example.com/data')
#             # Проверка на ошибки HTTP
#             response.raise_for_status()
#             data = response.json()
#             # Обработка полученных данных
#             return Response(data)
#         except RequestException as e:
#             # Обработка исключения
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
