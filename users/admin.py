from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'is_staff', 'is_active', 'date_joined',)
    list_filter = ('is_staff', 'is_active',)
    search_fields = ('email', 'phone',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'course', 'lesson', 'amount', 'payment_method',)
    list_filter = ('user', 'date',)
    search_fields = ('course', 'lesson',)