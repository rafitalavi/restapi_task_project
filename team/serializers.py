from rest_framework import serializers
from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField( read_only=True)
    members = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='profile-detail')
    manager = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='profile-detail')
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'image', 'created_at', 'updated_at', 'manager','members', 'members_count','points', 
                  'complted_projects', 'not_completed_projects' ,'url']
        read_only_fields = ['points', 'complted_projects', 'not_completed_projects']