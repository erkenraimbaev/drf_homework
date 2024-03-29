from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='media/', verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, related_name='courses_owner',
                              verbose_name='автор', **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='цена', default=5000, **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.description}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='media/', verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    link_to_video = models.CharField(max_length=150, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='курс', **NULLABLE)
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, related_name='lessons_owner',
                              verbose_name='автор', **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='цена', default=1000, **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.description}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class CourseSubscribe(models.Model):
    user = models.ForeignKey('users.User', related_name='user_sub', on_delete=models.CASCADE,
                             verbose_name='пользователь')
    course = models.ForeignKey(Course, related_name='course_sub', on_delete=models.CASCADE,
                               verbose_name='курс подписки')

    def __str__(self):
        return f'{self.user} {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
