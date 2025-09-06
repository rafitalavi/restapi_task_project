from django.contrib import admin
from .models import TaskList, Task, Attachment

# Register your models here.
class TaskListAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at', 'completed_on', 'created_by')
    list_display = ('id', 'name', 'status', 'team', 'created_by', 'created_at', 'completed_on')
    search_fields = ('name', 'status', 'team__name', 'created_by__user__username')
    ordering = ('-created_at',)
admin.site.register(TaskList, TaskListAdmin)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at', 'completed_on', 'created_by', 'completed_by')
    list_display = ('id', 'title', 'status', 'task_list', 'created_by', 'completed_by', 'created_at', 'completed_on')
    search_fields = ('title', 'status', 'task_list__name', 'created_by__user__username', 'completed_by__user__username')
    ordering = ('-created_at',)
admin.site.register(Task, TaskAdmin)
class AttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'uploaded_at',)
    list_display = ('id', 'file', 'task', 'uploaded_at')
    search_fields = ('task__title',)
    ordering = ('-uploaded_at',)    
admin.site.register(Attachment, AttachmentAdmin)