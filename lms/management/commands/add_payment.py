from datetime import datetime

from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email='testemail3@mail.ru', first_name='Test', last_name='Testov')

        course = Course.objects.create(title='test', description='test course')

        lesson = Lesson.objects.create(title='test lesson', description='test lesson', course=course)

        payment = Payment.objects.create(
            user=user,
            date=datetime.now(),
            course=course,
            lesson=lesson,
            amount=10000,
            payment_method='cache'
        )

        self.stdout.write(self.style.SUCCESS('Successfully created sample payments'))
