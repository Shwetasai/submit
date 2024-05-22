from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assigner = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'task', 'description', 'assignee', 'assigner', 'is_completed', 'created_at', 'updated_at']

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
