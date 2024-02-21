from django.contrib import admin

from lms.models import Course, Lesson, CourseSubscribe


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    list_filter = ('title',)
    search_fields = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    list_filter = ('title',)
    search_fields = ('title',)


@admin.register(CourseSubscribe)
class CourseSubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'course',)
    list_filter = ('course',)
    search_fields = ('user', 'course',)
