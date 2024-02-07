from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=50, verbose_name='номер телефона', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='страна', **NULLABLE)
    is_staff = models.BooleanField(default=False, verbose_name='статус персонала',
                                   help_text=_(
                                       "Определяет, может ли пользователь войти на этот сайт администрирования"),
                                   )
    is_active = models.BooleanField(default=True, verbose_name='активный пользовавтель',
                                    help_text=_(
                                        "Определяет, следует ли считать этого пользователя активным.")
                                    )
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата подключения')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
