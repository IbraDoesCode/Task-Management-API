from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import TaskSerializer, UserSerializer
from .models import User, Task
from .permissions import IsAssigned
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserLogin(APIView):
    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            # Implement token based
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserListCreate(APIView):
    # Here we ensure only authenticated and admin users can access this view
    permission_classes=[IsAuthenticated, IsAdminUser]

    #Get all users
    def get(self, request):
        # Get all users
        users = User.objects.all()
        # Serialize the users object to json
        serializer = UserSerializer(users, many=True)
        #return the serialized data
        return Response(serializer.data)

    #Create a new user
    def post(self, request):
        
        #Serialize the request data into user object
        serializer = UserSerializer(data=request.data)

        #Check if the data is valid
        if serializer.is_valid():
           
           #Get data from the serializer
            user_data = serializer.validated_data

            #Create and save the new user
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )

            #Serialize the user object
            user_serializer = UserSerializer(user)

            # Return serialized user object
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskListCreate(APIView):
    # Here we ensure only authenticated and assigned users can access this view
    permission_classes = [IsAuthenticated, IsAssigned]

    #Get all tasks
    def get(self, request):

        # if user is admin get all tasks, else get only tasks assigned to the user
        if request.user.is_staff:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(assigned_to=request.user)

        # serialize the tasks object to json
        serializer = TaskSerializer(tasks, many=True)

        # return the serialized data
        return Response(serializer.data)
        
    # Create a new task
    def post(self, request):

        # Ensure only admin can add tasks
        if not request.user.is_staff:
            return Response({'message': 'You do not have permission to add tasks'}, status=status.HTTP_403_FORBIDDEN)

        # Serialize the request data into task object
        serializer = TaskSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            # Serialize and save the task
            serializer.save()

            # Return the serialized task object
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskDetailView(APIView):
    #Ensure only authenticated and assigned users can this access view
    permission_classes = [IsAuthenticated, IsAssigned]

    def get(self, request, pk):
        try:
            # Get the task object
            task = Task.objects.get(pk=pk)

            # Check if the user is assigned to the task or is an admin
            if request.user.is_staff or task.assigned_to == request.user:
                #Serialize the task object
                serializer = TaskSerializer(task)
                # Return the serialized task object
                return Response(serializer.data)
            else:
                return Response({'message': 'You do not have permission to view this task.'}, status=status.HTTP_403_FORBIDDEN)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, pk):
        try:
            # Get the task object
            task = Task.objects.get(pk=pk)
            # Check if the user is assigned to the task or is an admin
            if request.user.is_staff or task.assigned_to == request.user:
                task.is_completed = True
                task.save()

                # Serialize the task object
                serializer = TaskSerializer(task)

                # Return the serialized task object
                return Response(serializer.data)
            else:
                return Response({'message': 'You do not have permission to complete this task.'}, status=status.HTTP_403_FORBIDDEN)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            # Get the task object
            task = Task.objects.get(pk=pk)

            #Check if the user is assigned to the task or is an admin
            if request.user.is_staff() or task.assigned_to == request.user:
                task.is_completed = True
                task.delete()

                serializer = TaskSerializer(task)
                return Response(serializer.data)
            else:
                return Response({'message': 'You do not have the permission to delete this task '}, status=status.HTTP_403_FORBIDDEN)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)