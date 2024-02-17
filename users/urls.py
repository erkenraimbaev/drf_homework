from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListView, MyTokenObtainPairView

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [path('', include(router.urls)),
               path('payments/', PaymentListView.as_view(), name='payments'),
               path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
               path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
               ]
