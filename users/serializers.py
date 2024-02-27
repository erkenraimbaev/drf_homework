from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.fields import SerializerMethodField

from users.models import User, Payment
from users.services import  get_link_to_payment


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

    class Meta:
        model = Payment
        fields = '__all__'

    def get_payment_url(self, instance):
        if instance.lesson:
            buy_object = instance.lesson
        else:
            buy_object = instance.course
        session = get_link_to_payment(course_title=buy_object.title, course_price=buy_object.price)
        return session
