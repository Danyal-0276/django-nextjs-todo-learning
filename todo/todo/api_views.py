from rest_framework import permissions, viewsets
from todo.models import Todo
from todo.serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return Todo.objects.filter(
            user=self.request.user,
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
