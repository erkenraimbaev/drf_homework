from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from lms.models import Course, CourseSubscribe


@shared_task
def send_course_update(course_id: int, message: str):
    course = Course.objects.get(pk=course_id)
    sub_courses = CourseSubscribe.objects.filter(course=course_id)
    for sub in sub_courses:
        send_mail(subject=f"Обновился курс {course.title}!",
                  message=message,
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[f'{sub.user}'],
                  fail_silently=True
                  )
