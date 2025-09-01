from rest_framework import viewsets
from .models import Team

from .serializers import TeamSerializer
from .permissions import IsTeamManagerOrReadOnly

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    permission_classes = [IsTeamManagerOrReadOnly]
    serializer_class = TeamSerializer