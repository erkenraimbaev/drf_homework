# Generated by Django 4.2.7 on 2024-02-07 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='название')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='изображение')),
                ('description', models.TextField(verbose_name='описание')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='название')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='изображение')),
                ('description', models.TextField(verbose_name='описание')),
                ('link_to_video', models.CharField(max_length=150, verbose_name='ссылка на видео')),
                ('course', models.ForeignKey(default='Неизвестный курс', on_delete=django.db.models.deletion.SET_DEFAULT, to='lms.course', verbose_name='курс')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
    ]
