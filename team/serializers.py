from rest_framework import serializers
from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField( read_only=True)
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'image', 'created_at', 'updated_at', 'manager', 'members_count','points', 
                  'complted_projects', 'not_completed_projects']
        read_only_fields = ['points', 'complted_projects', 'not_completed_projects']