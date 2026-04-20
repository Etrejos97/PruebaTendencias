from rest_framework import viewsets, permissions
from .models import Task, Tag, Comment
from .serializers import TaskSerializer, TagSerializer, CommentSerializer
from projects.models import ProjectMembership
from projects.permissions import IsProjectMember, IsProjectEditorOrOwner


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember, IsProjectEditorOrOwner]
    filterset_fields = ['project', 'status', 'priority', 'assigned_to', 'is_active', 'tags__name']
    search_fields = ['title', 'description', 'tags__name']
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        member_projects = ProjectMembership.objects.filter(
            user=user
        ).values_list('project_id', flat=True)
        return Task.objects.filter(project__in=member_projects)


