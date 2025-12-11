# tasks/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

# Task serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at', 'owner']
        read_only_fields = ['owner', 'created_at', 'updated_at']

# User registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
