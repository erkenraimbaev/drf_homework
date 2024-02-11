from django.urls import path, include
from rest_framework import routers

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListView

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [path('', include(router.urls)),
               path('payments/', PaymentListView.as_view(), name='payments'),
               ]
