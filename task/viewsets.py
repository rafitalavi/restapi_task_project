from rest_framework import viewsets, mixins ,response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status as drf_status
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .models import TaskList, Task, Attachment
from .models import NOT_COMPLETED, IN_PROGRESS, COMPLETED
from rest_framework.decorators import action
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
        if getattr(user_profile, "role", None) == "manager":
            # Get all teams managed by this profile
            return TaskList.objects.filter(team__in=user_profile.teams.all())
        else:
            # Members see only their own team’s task lists
            return TaskList.objects.filter(team=user_profile.team)


    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        serializer.save(created_by=user_profile, team=user_profile.team)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAllowedToEditTaskElseNone]
    queryset = Task.objects.all()  # required for DRF router
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['status', ]

    def get_queryset(self):
        user_profile = self.request.user.profile
        if getattr(user_profile, "role", None) == "manager":
            return Task.objects.filter(task_list__team__in=user_profile.teams.all())
        else:
            return Task.objects.filter(task_list__team=user_profile.team)


    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        # Only managers can create tasks
        if getattr(user_profile, "role", None) != "manager":
            raise PermissionDenied("Only managers can create tasks.")
        serializer.save(created_by=user_profile)
    @action(detail=True, methods=['patch'])
    def update_task_status(self, request, pk=None):
        try:
            task  = self.get_object()
            profile = request.user.profile
            status = request.data.get('status')
            if (status  == NOT_COMPLETED ):
                if (status == COMPLETED ):
                    task.status = NOT_COMPLETED
                    task.completed_by = None
                    task.completed_on = None
                else:
                    raise PermissionDenied(" task is completed or in progress.")
            elif (status == COMPLETED):
                if (task.status == NOT_COMPLETED):
                    task.status = COMPLETED
                    
                    task.completed_by = None
                    task.completed_on = timezone.now()
                    task.completed_by = profile
                else:
                    raise PermissionDenied(" task is Already completed .")     
            else:
                raise PermissionDenied("Invalid status value.")    
            task.save()
            serializer = TaskSerializer(instance=task , context={'request': request})    
            return response.Response(serializer.data, status=drf_status.HTTP_200_OK)
        except Exception as e:
             return response.Response(
        {"detail": str(e)},
        status=drf_status.HTTP_400_BAD_REQUEST
    )


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
