from django.db import models
from users.models import Profile
import uuid
from  django.utils.deconstruct import deconstructible
import os
# Create your models here.
NOT_COMPLETED = 'NC'
COMPLETED = 'C'
IN_PROGRESS = 'IP'
STATUS_CHOICES = [
    (NOT_COMPLETED, 'Not Completed'),   
    (COMPLETED, 'Completed'),
    (IN_PROGRESS, 'In Progress'),   
]
@deconstructible
class GenerateAttachmentFilePath:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        task_title = instance.task.title if instance.task else "untitled"
        path = f'task_list_images/{task_title}/attachments'
        name = f'{task_title}_attachments.{ext}'
        return os.path.join(path, name)

filePath = GenerateAttachmentFilePath()
class TaskList(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True, default=None)
    team = models.ForeignKey('team.Team', on_delete=models.CASCADE, related_name='task_lists', null=True, blank=True)
    created_by = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, related_name='created_task_lists' , null=True, blank=True  )
    status = models.CharField(max_length=50, default=NOT_COMPLETED, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.id} | {self.name} | {self.status}"

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    completed_on = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, related_name='created_by' , null=True, blank=True  )
    completed_by = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, related_name='completed_tasks' , null=True, blank=True  ) 
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True) 
    status = models.CharField(max_length=50, default=NOT_COMPLETED, choices=STATUS_CHOICES)
    def __str__(self):
        return f"{self.id} | {self.title} | {self.status}"

class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=filePath, blank=True, null=True   )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')

    def __str__(self):
        return f"Attachment {self.id} for Task {self.task}"