from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    pass

class Task(models.Model):
    task = models.CharField(max_length=255)
    description = models.TextField()
    assignee = models.ForeignKey(CustomUser, related_name='assigned_tasks', on_delete=models.CASCADE)
    assigner = models.ForeignKey(CustomUser, related_name='assigned_by', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task
