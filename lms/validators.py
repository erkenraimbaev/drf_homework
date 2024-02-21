from rest_framework import serializers


class UrlFieldValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if 'youtube.com' not in value.get(self.field, ''):
            raise serializers.ValidationError("Ссылка должна быть из 'youtube.com'")
