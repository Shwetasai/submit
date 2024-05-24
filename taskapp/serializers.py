from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task,Feedback

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email','role']

class TaskSerializer(serializers.ModelSerializer):
    assigner = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'task', 'description', 'assignee', 'assigner', 'is_completed', 'created_at', 'updated_at']

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password','role']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'employee') 
        )
        return user

class FeedbackSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'task', 'manager', 'feedback', 'created_at']