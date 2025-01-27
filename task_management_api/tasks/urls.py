from django.urls import path
from .views import UserListCreate, TaskListCreate, UserLogin, TaskDetailView

urlpatterns = [
    path('login/', UserLogin.as_view(), name='user-login'),
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-list-create'),
]

