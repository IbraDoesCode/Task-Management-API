from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task (models.Model):
    title = models.CharField(max_length=255)  # Task title with a max length
    description = models.TextField()  # Optional detailed task description
    assigned_to = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set creation timestamp
    is_completed = models.BooleanField(default=False)  # Task completion status
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set update timestamp

    def __str__(self):
        return f'Task: {self.title} - Assigned to: {self.assigned_to.username} status: {self.is_completed}'
