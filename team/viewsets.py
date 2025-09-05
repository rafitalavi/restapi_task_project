from rest_framework import viewsets ,status
from .models import Team
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import TeamSerializer
from .permissions import IsTeamManagerOrReadOnly

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    permission_classes = [IsTeamManagerOrReadOnly]
    serializer_class = TeamSerializer
    @action(detail=True, methods=['post'] ,name = 'join' ,  permission_classes= []) 
    def join(self ,request, pk=None):
       try:
           team = self.get_object()
           profile = request.user.profile
           if profile.team is not None:
               profile.team = team
               profile.save()
               return Response( status=status.HTTP_204_NO_CONTENT)
           elif profile in team.members.all():
               return Response({'detail': 'You are already a member of this team.'}, status=status.HTTP_400_BAD_REQUEST)
           else: 
                 return Response({'detail': 'You are already a member of other team.'}, status=status.HTTP_400_BAD_REQUEST)
       except Exception as e   :
               return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(detail=True, methods=['post'] ,name = 'leave', permission_classes= []) 
    def leave(self ,request, pk=None):
         try:
           team = self.get_object()
           profile = request.user.profile
           if profile.team == team:
               profile.team = None
               profile.save()
               return Response( status=status.HTTP_204_NO_CONTENT)
           else: 
                 return Response({'detail': 'You are not a member of this team.'}, status=status.HTTP_400_BAD_REQUEST)
         except Exception as e   :
               return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
       