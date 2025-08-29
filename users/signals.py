from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(pre_save, sender=User)
@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        base_username = f'{instance.first_name}_{instance.last_name}'.lower()
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f'{base_username}{counter}'
            counter += 1

        instance.username = username
