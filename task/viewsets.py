from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from .models import TaskList, Task, Attachment
from .serializers import TaskListSerializer, TaskSerializer, AttachmentSerializer
from .permissions import (
    IsAllowedToEditTaskListElseNone,
    IsAllowedToEditTaskElseNone,
    IsAllowedToEditAttachmentElseNone,
)


class TaskListViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,  # enable listing
    viewsets.GenericViewSet,
):
    serializer_class = TaskListSerializer
    permission_classes = [IsAllowedToEditTaskListElseNone]
    queryset = TaskList.objects.all()  # required for DRF router

    def get_queryset(self):
        user_profile = self.request.user.profile
        return TaskList.objects.filter(team=user_profile.team)

    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        serializer.save(created_by=user_profile, team=user_profile.team)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAllowedToEditTaskElseNone]
    queryset = Task.objects.all()  # required for DRF router

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Task.objects.filter(task_list__team=user_profile.team)

    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        # Only managers can create tasks
        if getattr(user_profile, "role", None) != "manager":
            raise PermissionDenied("Only managers can create tasks.")
        serializer.save(created_by=user_profile)


class AttachmentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,  # optional: list attachments
    viewsets.GenericViewSet,
):
    serializer_class = AttachmentSerializer
    permission_classes = [IsAllowedToEditAttachmentElseNone]
    queryset = Attachment.objects.all()  # required for DRF router

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Attachment.objects.filter(task__task_list__team=user_profile.team)
