from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import Task, Feedback, CustomUser
from .serializers import TaskSerializer, RegistrationSerializer, FeedbackSerializer
from .decorators import admin_required

def get_object_or_404(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        raise Http404

class TaskListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(assigner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        if task.assignee != request.user:
            return Response({'error': 'Only the assigned employee can update the task status.'}, status=status.HTTP_403_FORBIDDEN)
        task.is_completed = True
        task.save()
        return Response({'status': 'Task marked as completed'}, status=status.HTTP_200_OK)

class FeedbackView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @admin_required
    def post(self, request, *args, **kwargs):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.validated_data['task']
            if request.user.role != CustomUser.MANAGER:
                return Response({'error': 'Only managers can give feedback.'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save(manager=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
