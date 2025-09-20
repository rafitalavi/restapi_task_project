from django.db import models
import os
import uuid
from django.utils.deconstruct import deconstructible



@deconstructible
class GenerateTeamImagePath:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'team_images/{instance.name}/image'
        name = f'{instance.name}_image.{ext}'
        return os.path.join(path, name)
ImageFilePath = GenerateTeamImagePath()
class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to=ImageFilePath, blank=True, null=True)  # ❌ remove ()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name='teams', null=True, blank=True)
    
    points = models.IntegerField(default=0)
    complted_projects = models.IntegerField(default=0)
    not_completed_projects = models.IntegerField(default=0)
    total_projects = models.IntegerField(default=0)

    def __str__(self):
        return self.name
