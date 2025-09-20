# from rest_framework import serializers
# from .models import Team

# class TeamSerializer(serializers.ModelSerializer):
#     members_count = serializers.IntegerField( read_only=True)
#     members = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='profile-detail')
#     manager = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='profile-detail')
#     listed_projects = serializers.HyperlinkedRelatedField(
#         many=True, read_only=True, view_name='tasklist-detail', source='task_lists'
#     )

#     class Meta:
#         model = Team
#         fields = ['id', 'name', 'description', 'image', 'created_at', 'updated_at', 'manager','members', 'members_count','points', 
#                   'complted_projects', 'not_completed_projects' ,'url' ,'listed_projects']
#         read_only_fields = ['points', 'complted_projects', 'not_completed_projects']
from rest_framework import serializers
from .models import Team
from users.models import Profile  # assuming members are Profile objects

class TeamSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(read_only=True)

    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Profile.objects.all(), required=False
    )
    manager = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(), required=False
    )
    listed_projects = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='tasklist-detail', source='task_lists'
    )

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'image', 'created_at', 'updated_at',
            'manager', 'members', 'members_count', 'points',
            'complted_projects', 'not_completed_projects', 'url', 'listed_projects', 'total_projects'
        ]
        read_only_fields = ['points', 'complted_projects', 'not_completed_projects', 'total_projects']
