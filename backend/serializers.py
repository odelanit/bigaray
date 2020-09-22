from django.contrib.auth.models import User
from rest_framework import serializers


class UserInfo:
    def __init__(self, username, email, password, first_name, last_name, gender, birthday, country):
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birthday = birthday
        self.country = country


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.IntegerField()
    birthday = serializers.DateField(required=False, allow_null=True)
    country = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, data):
        try:
            User.objects.get(username=data['username'])
            raise serializers.ValidationError({
                "username": "username already taken"
            })
        except User.DoesNotExist:
            pass
        try:
            User.objects.get(username=data['email'])
            raise serializers.ValidationError({
                "email": "email already taken"
            })
        except User.DoesNotExist:
            pass
        return data
