from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'is_staff', 'is_active', 'date_joined',)
    list_filter = ('is_staff', 'is_active',)
    search_fields = ('email', 'phone',)
