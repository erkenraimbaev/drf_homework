from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.fields import SerializerMethodField

from users.models import User, Payment
from users.services import get_link_to_payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email

        return token


class PaymentSerializer(serializers.ModelSerializer):
    payment_url = SerializerMethodField()
    payment_session_id = SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    def buy_course_or_lesson(self, instance):
        """ Функция для получения обьекта курса или урока для совершения платежа"""
        if instance.lesson:
            buy_object = instance.lesson
        else:
            buy_object = instance.course
        session = get_link_to_payment(course_title=buy_object.title, course_price=buy_object.price)
        return session

    def get_payment_url(self, instance):
        session = self.buy_course_or_lesson(instance)
        return session.get('url')

    def get_payment_session_id(self, instance):
        session = self.buy_course_or_lesson(instance)
        return session.get('id')
