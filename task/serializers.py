from rest_framework import serializers
from .models import TaskList, Task, Attachment
from team.models import Team


class TaskListSerializer(serializers.ModelSerializer):
    team = serializers.HyperlinkedRelatedField( queryset = Team.objects.all(), view_name='team-detail', many=False)
    created_by = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='profile-detail')
    tasks = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='task-detail')
    class Meta:
        model = TaskList
        fields = ['id', 'name', 'description', 'status', 'created_at', 'updated_at', 'completed_on', 'team', 'tasks','created_by', 'tasks', 'url']
        read_only_fields = ['created_at', 'updated_at' ,'status']

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='profile-detail')
    completed_by = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='profile-detail')
    task_list = serializers.HyperlinkedRelatedField( queryset = TaskList.objects.all(), view_name='tasklist-detail', many=False)
    attachments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='attachment-detail')
    def validate_task_list(self, value):
        if value.status == 'completed':
            user_profile = self.context['request'].user.profile
            if value not in user_profile.team.task_lists.all():
                raise serializers.ValidationError("taske it not belong to your team")
        return value
    # def create(self, validated_data):
    #     user_profile = self.context['request'].user.profile
    #     task = Task.objects.create(created_by=user_profile, **validated_data)
    #     return task
    class Meta:
        model = Task
        fields = ['id', 'title', 'description','attachments', 'status', 'created_at', 'updated_at', 'completed_on', 'task_list', 'created_by', 'completed_by',  'url']
        read_only_fields = ['created_at', 'updated_at' , 'created_by', 'completed_by']




class AttachmentSerializer(serializers.ModelSerializer):
    task = serializers.HyperlinkedRelatedField(queryset=Task.objects.all(), view_name='task-detail')

    def validate(self, attrs):
        user_profile = self.context['request'].user.profile
        task = attrs.get('task')
        task_list = task.task_list
        if task_list not in user_profile.team.task_lists.all():
            raise serializers.ValidationError({"task": "Task does not belong to your team."})
        return attrs

    class Meta:
        model = Attachment
        fields = ['id', 'file', 'uploaded_at', 'task', 'url']
        read_only_fields = ['uploaded_at']



# class AttachmentSerializer(serializers.ModelSerializer):
#     task = serializers.HyperlinkedRelatedField(
#         queryset=Task.objects.all(), 
#         view_name='task-detail', 
#         many=False
#     )

#     def validate(self, attrs):
#         user_profile = self.context['request'].user.profile
#         task = attrs.get('task')
#         task_list = TaskList.objects.get(tasks__id__exact= task.id)  # directly get the task's task_list
#         if task_list not in user_profile.team.task_lists.all():
#             raise serializers.ValidationError({"task": "Task does not belong to your team."})
#         return attrs
   

#     class Meta:
#         model = Attachment
#         fields = ['id', 'file', 'uploaded_at', 'task', 'url']
#         read_only_fields = ['uploaded_at']
