from django.contrib.auth.models import User
from rest_framework import serializers

class SignupSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

class SigninSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

class InfoSerializer(serializers.Serializer):
    id = serializers.CharField(source='username')
    id_type = serializers.CharField(source='profile.id_type')

class LogoutSerializer(serializers.Serializer):
    all = serializers.BooleanField()
