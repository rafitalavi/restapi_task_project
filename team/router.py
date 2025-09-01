from rest_framework import viewsets
from .models import Team
from .serializers import TeamSerializer
from .viewsets import TeamViewSet
from rest_framework import routers


app_name = 'team'
router = routers.DefaultRouter()
router.register(r'team', TeamViewSet)