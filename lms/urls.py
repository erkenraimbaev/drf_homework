from django.urls import path, include
from rest_framework import routers

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonListView, LessonDetailView, LessonCreateView, LessonUpdateView, \
    LessonDeleteView, CourseSubscribeCreateAPIView, CourseSubscribeDestroyAPIView, CourseSubscribeListAPIView, \
    CourseSubscribePostAPIView

app_name = LmsConfig.name

router = routers.DefaultRouter()
router.register(r'lms', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson-delete'),
    path('subscribe/', CourseSubscribeCreateAPIView.as_view(), name='subscribe'),
    path('unsubscribe/<int:pk>/', CourseSubscribeDestroyAPIView.as_view(), name='unsubscribe'),
    path('subscribe_list/', CourseSubscribeListAPIView.as_view(), name='subscribe_list'),
    path('subscribe_course/<int:course_id>/', CourseSubscribePostAPIView.as_view(), name='subscribe_course'),
]
