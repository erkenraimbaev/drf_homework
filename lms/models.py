from django.db import models
NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='media/', verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание')

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
    course = models.ForeignKey(Course, on_delete=models.SET_DEFAULT, default='Неизвестный курс', verbose_name='курс')

    def __str__(self):
        return f'{self.title} {self.description}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
