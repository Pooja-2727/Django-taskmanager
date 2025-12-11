# tasks/views.py
from rest_framework import viewsets, generics, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Task
from .serializers import TaskSerializer, RegisterSerializer
from .permissions import IsOwnerOrAdmin

User = get_user_model()

# ------------------------------
# User Registration
# ------------------------------
class RegisterView(generics.CreateAPIView):
    """
    Endpoint for registering a new user.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# ------------------------------
# Task CRUD + Toggle
# ------------------------------
class TaskViewSet(viewsets.ModelViewSet):
    """
    list: Admin -> all tasks; User -> own tasks only
    retrieve/update/destroy: restricted by IsOwnerOrAdmin
    toggle: mark complete/incomplete
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Admin").exists() or user.is_superuser:
            qs = Task.objects.all()
            # Optional: filter by owner via query param ?owner=username
            owner = self.request.query_params.get("owner")
            if owner:
                qs = qs.filter(owner__username=owner)
            return qs
        # Regular users see only their own tasks
        return Task.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsOwnerOrAdmin])
    def toggle(self, request, pk=None):
        """
        Custom action to toggle task completion status
        """
        task = self.get_object()
        task.status = not task.status
        task.save()
        return Response(self.get_serializer(task).data)
