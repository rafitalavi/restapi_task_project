from rest_framework import routers
from .viewsets import UserViewSet

app_name = 'users' #namespace for the users app exactly like app name
router = routers.DefaultRouter() #creating a router object
router.register(r'users', UserViewSet) #registering the UserViewSet with the router
urlpatterns = router.urls #assigning the router urls to urlpatterns like urls.py  
