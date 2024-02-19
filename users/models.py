from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

from lms.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=50, verbose_name='номер телефона', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):

    PAYMENT_METHOD = [
        ('cache', 'Наличными'),
        ('card', 'перевод на счет')
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='пользователь', **NULLABLE)
    date = models.DateTimeField(default=datetime.now, verbose_name='дата')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='курс', related_name='lessons',
                               **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name='урок', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='цена')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, verbose_name='способ оплаты')

    def __str__(self):
        return f"{self.user} on  {self.date}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
