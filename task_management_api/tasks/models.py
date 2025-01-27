from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task (models.Model):
    title = models.CharField(max_length=255)  
    description = models.TextField()  
    assigned_to = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE) # Here we are referencing to Django's built-in User model
    created_at = models.DateTimeField(auto_now_add=True)  
    is_completed = models.BooleanField(default=False)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'Task: {self.title} - Assigned to: {self.assigned_to.username} status: {self.is_completed}'
