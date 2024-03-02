from datetime import datetime, timedelta

from celery import shared_task

from users.models import User


@shared_task
def user_blocker():
    month_ago = datetime.now() - timedelta(days=30)

    for not_active_user in User.objects.filter(
            last_login__lte=month_ago, is_active=True):
        not_active_user.is_active = False
        not_active_user.save()
