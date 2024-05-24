from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    MANAGER = 'manager'
    EMPLOYEE = 'employee'
    ROLE_CHOICES = [
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=EMPLOYEE)


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

class Feedback(models.Model):
    task = models.ForeignKey(Task, related_name='feedbacks', on_delete=models.CASCADE)
    manager = models.ForeignKey(CustomUser, related_name='feedback_given', on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback for {self.task.task} by {self.manager.username}'