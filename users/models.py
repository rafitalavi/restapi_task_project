from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible


import os
# Create your models here.
@deconstructible
class UploadToPathAndRename:
    def __init__(self, path):
        pass

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/accounts/{instance.user.id}/images/'
        filename = f'profile_image.{ext}'
        return os.path.join(path, filename)
class Profile(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('member', 'Member'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=UploadToPathAndRename('media/accounts/'), blank=True, null=True)
    team = models.ForeignKey('team.Team', on_delete=models.SET_NULL, related_name='members', null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member'
    )
   

    def __str__(self):
        return f'{self.user.username} Profile'
