from rest_framework import serializers
from .models import Task, User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # This will not be returned in response
    
    class Meta:
        model = User
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = '__all__'