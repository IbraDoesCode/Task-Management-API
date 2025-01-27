from rest_framework.permissions import BasePermission

# This permission class ensures that the tasks is assigned to the request user
class IsAssigned(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned == request.user