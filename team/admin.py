from django.contrib import admin

# Register your models here.
from .models import Team
from .serializers import TeamSerializer

class TeamAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at', 'points', 'complted_projects', 'not_completed_projects')
    list_display = ('id', 'name', 'manager', 'points', 'complted_projects', 'not_completed_projects', )
    search_fields = ('name', 'manager__username')
    ordering = ('-created_at',)
admin.site.register(Team, TeamAdmin)
