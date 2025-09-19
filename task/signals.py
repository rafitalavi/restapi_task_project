from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Task, COMPLETED, IN_PROGRESS, NOT_COMPLETED
from django.utils import timezone
@receiver(post_save, sender=Task)
def update_team_point(sender, instance, created, **kwargs):
    team = instance.task_list.team 
    if instance.status == COMPLETED:
        team.points += 10
        team.complted_projects += 1
    elif instance.status == NOT_COMPLETED:
        if team.points >= 10:
            team.points -= 5
    team.save(update_fields=["points", "complted_projects"])

def update_task_list_status(task_list):
    tasks = task_list.tasks.all()

    if not tasks.exists():
        # No tasks in the list → consider as NOT_COMPLETED
        task_list.status = NOT_COMPLETED
        task_list.completed_on = None
    else:
        all_completed = all(task.status == COMPLETED for task in tasks)
        any_completed = any(task.status == COMPLETED for task in tasks)

        if all_completed:
            task_list.status = COMPLETED
            task_list.completed_on = timezone.now()
        elif any_completed:
            task_list.status = IN_PROGRESS
            task_list.completed_on = None
        else:
            task_list.status = NOT_COMPLETED
            task_list.completed_on = None

    task_list.save(update_fields=["status", "completed_on", "updated_at"])


@receiver(post_save, sender=Task)
def update_task_list_status_on_task_save(sender, instance, created, **kwargs):
    update_task_list_status(instance.task_list)


@receiver(post_delete, sender=Task)
def update_task_list_status_on_task_delete(sender, instance, **kwargs):
    update_task_list_status(instance.task_list)
