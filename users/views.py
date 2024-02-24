from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from lms.models import Course
from users.models import User
from users.serializers import UserSerializer, MyTokenObtainPairSerializer

from users.models import Payment
from users.serializers import PaymentSerializer

from django_filters.rest_framework import DjangoFilterBackend
from config.settings import API_KEY_STRIPE
import stripe

from users.services import get_link_to_payment, get_session


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('date',)


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, requests, *args, **kwargs):
        payment = Payment()
        buy_object = Course.objects.filter(id=payment.course)
        print(buy_object)
        name = buy_object.get("title")
        price = buy_object.get("price")
        session = get_link_to_payment(course_title=name, course_price=price)
        payment.session_id = session.get('id')
        payment.amount = price
        return session.get('url')


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        not_paid_payments = Payment.objects.filter(payment_status="open")
        for payment in not_paid_payments:
            session = get_session(payment.session_id)
            if session.payment_status in ['paid', 'expired']:
                payment.save()
        return self.retrieve(request, *args, **kwargs)
