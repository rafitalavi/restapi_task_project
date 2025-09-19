from rest_framework import routers
from .viewsets import TaskListViewSet, TaskViewSet, AttachmentViewSet

app_name = 'task'
router = routers.DefaultRouter()

# Add basename explicitly for ViewSets without a queryset attribute
router.register('task-lists', TaskListViewSet, basename='tasklist')
router.register('tasks', TaskViewSet, basename='task')
router.register('attachments', AttachmentViewSet, basename='attachment')
