from django.contrib import admin
from .models import Task, CustomUser

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['task', 'assignee', 'assigner', 'is_completed', 'created_at', 'updated_at']
    search_fields = ['task', 'description']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff','role']
    search_fields = ['username', 'email']
