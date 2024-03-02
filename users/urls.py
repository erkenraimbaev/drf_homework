from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentListView, MyTokenObtainPairView, UserListView, UserDetailView, UserCreateView, \
    UserUpdateView, UserDeleteView, PaymentCreateView, PaymentDetailView

app_name = UsersConfig.name

urlpatterns = [path('users/', UserListView.as_view(), name='users-list'),
               path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
               path('create/', UserCreateView.as_view(), name='users-create'),
               path('update/<int:pk>/', UserUpdateView.as_view(), name='users-update'),
               path('delete/<int:pk>/', UserDeleteView.as_view(), name='users-delete'),
               path('payments/', PaymentListView.as_view(), name='payments'),
               path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
               path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
               path('course_or_lesson/buy/', PaymentCreateView.as_view(), name='course_buy'),
               ]
