from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course, CourseSubscribe
from users.models import User


class LessonTestCase(APITestCase):
    """ Тестирование механизма CRUD для уроков"""

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test_email@mail.ru',
            password='Parol1234'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='Test lesson1',
            description='Test',
            link_to_video='https://youtube.com/videoo',
        )

    def test_get_lesson_list(self):
        """ Тестирование получения списка студентов"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/lessons/')

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_lesson_update(self):
        """ Тест для обновления урока"""

        self.client.force_authenticate(user=self.user)

        updated_data = {
            'title': 'Another lesson',
            'description': 'Test changes',
            'link_to_video': 'https://youtube.com/video2/',
            'course': self.course.id,
        }

        response = self.client.put(f'/lessons/update/{self.lesson.pk}/',
                                   data=updated_data
                                   )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.lesson.refresh_from_db()
        self.assertEqual(
            self.lesson.title,
            updated_data['title']
        )

        self.lesson.refresh_from_db()
        self.assertEqual(
            self.lesson.description,
            updated_data['description']
        )

    def test_lesson_create(self):
        """ Тест для создания урока"""

        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Test lesson',
            'description': 'Test',
            'link_to_video': 'https://youtube.com/video',
            'course': self.course.id,
            'user': self.user.id
        }

        response = self.client.post('/lessons/create/',
                                    data=data
                                    )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_destroy_lesson(self):
        """ Тест для удаления урока"""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f'/lessons/delete/{str(self.lesson.pk)}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CourseSubscribeTestCase(APITestCase):
    """ Тест для подписки"""

    def setUp(self):
        self.user = User.objects.create(email='test2@email.ru', password='password')
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        self.subscribe = CourseSubscribe.objects.create(
                                                        user=self.user,
                                                        course=self.course
                                                        )

    def test_get_subscribe_list_authenticated(self):
        """ Тест для получения списка подписок"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/subscribe_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_subscribe_authenticated(self):
        """ Тест для добавления и отмены подписки"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/subscribe_course/{self.course.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_course_subscription_unauthenticated(self):
        """ Тест для неавторизованного пользователя"""
        response = self.client.post('/subscribe/'.format(self.course.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
