from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer , ProfileSerializer
from .permissions import IsUserOwnerOrGetAndPostOnly , IsProfileOwnerOrReadOnly
from .models import Profile
class UserViewSet(viewsets.ModelViewSet):# provides list, create, retrieve, update, destroy actions modelviewset
    permission_classes = [IsUserOwnerOrGetAndPostOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.GenericViewSet , viewsets.mixins.RetrieveModelMixin, viewsets.mixins.UpdateModelMixin,
                    #   viewsets.mixins.ListModelMixin, viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin
                      ):
    permission_classes = [IsProfileOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer