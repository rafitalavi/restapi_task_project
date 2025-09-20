from background_task import background
from background_task.tasks import Task as BT
from task.models import Task , COMPLETED, IN_PROGRESS, NOT_COMPLETED
from django.utils import timezone
from team.models import Team
@background(schedule=10)
def update_team_stat():
    for team in Team.objects.all():
        total_projects = 0
        complted_projects = 0
        not_completed_projects = total_projects - complted_projects
        for task_list in team.task_lists.all():
            total_projects += task_list.tasks.count()
            complted_projects += task_list.tasks.filter(status=COMPLETED).count()
        team.total_projects = total_projects
        team.complted_projects = complted_projects
        team.not_completed_projects = total_projects - complted_projects
        team.save(update_fields=['total_projects', 'complted_projects', 'not_completed_projects'])
if not BT.objects.filter(verbose_name = 'update_team_stat').exists():           
    update_team_stat(repeat=BT.DAILY ,verbose_name = 'update_team_stat', priority = 0 )  # Repeat every hour