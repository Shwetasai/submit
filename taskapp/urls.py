from django.urls import path
from .views import TaskListCreateView, TaskDetailView, RegistrationView, TaskStatusUpdateView, FeedbackView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/', TaskListCreateView.as_view(), name='task_list_create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/complete/', TaskStatusUpdateView.as_view(), name='task_status_update'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
]
