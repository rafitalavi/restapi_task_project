from rest_framework import viewsets, status
from .models import Team
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import TeamSerializer
from .permissions import IsTeamManagerOrReadOnly
from django.contrib.auth.models import User 


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    permission_classes = [IsTeamManagerOrReadOnly]
    serializer_class = TeamSerializer

    @action(detail=True, methods=['post'], url_path='join', permission_classes=[]) 
    def join(self, request, pk=None):
        try:
            team = self.get_object()
            profile = request.user.profile

            if profile.team is None:
                profile.team = team
                profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

            elif profile.team == team:
                return Response({'detail': 'You are already a member of this team.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'detail': 'You are already a member of other team.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='leave', permission_classes=[]) 
    def leave(self, request, pk=None):
        try:
            team = self.get_object()
            profile = request.user.profile

            if profile.team == team:
                profile.team = None
                profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

            else:
                return Response({'detail': 'You are not a member of this team.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    from rest_framework import viewsets, status
from .models import Team
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import TeamSerializer
from .permissions import IsTeamManagerOrReadOnly


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    permission_classes = [IsTeamManagerOrReadOnly]
    serializer_class = TeamSerializer

    @action(detail=True, methods=['post'], url_path='join', permission_classes=[]) 
    def join(self, request, pk=None):
        try:
            team = self.get_object()
            profile = request.user.profile

            if profile.team is None:
                profile.team = team
                profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

            elif profile.team == team:
                return Response({'detail': 'You are already a member of this team.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'detail': 'You are already a member of other team.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='leave', permission_classes=[]) 
    def leave(self, request, pk=None):
        try:
            team = self.get_object()
            profile = request.user.profile

            if profile.team == team:
                profile.team = None
                profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

            else:
                return Response({'detail': 'You are not a member of this team.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(detail=True, methods=['post'], url_path='remove-member',)
    def remove_member(self, request, pk=None):
        try:
            team = self.get_object()
            profile_id = request.data.get('profile_id', None)
            

            if not profile_id:
                return Response({'detail': 'Profile ID is required.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            profile = User.objects.get(id=profile_id).profile
            team_members = team.members
            if (profile in  team_members.all()):
                team_members.remove(profile)
                team.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': 'Profile not found in this team.'}, 
                                status=status.HTTP_404_NOT_FOUND)
    

         

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
