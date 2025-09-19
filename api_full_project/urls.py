"""
URL configuration for api_full_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path , include
from users import router as user_api_router  
from team import router as team_api_router 
from task import router as task_api_router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

auth_api_url_patterns = [
    path('', include('dj_rest_auth.urls')),   # /api/auth/login/
    path('token/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]

if settings.DEBUG:
    auth_api_url_patterns.append(path('verify/', include('rest_framework.urls')) ) # DRF login/logout views for the browsable API)
api_url_patterns = [
    # Including the team app router URLs under 'teams/' path
    path('auth/', include(auth_api_url_patterns)),  # Including the auth API URL patterns
    path('accounts/', include(user_api_router.router.urls)),  # Including the users app router URLs under 'accounts/' path
    path('teams/', include(team_api_router.router.urls)), 
    path('tasks/', include(task_api_router.router.urls)),  # Including the task app router URLs under 'tasks/' path
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_url_patterns)),  # Including the API URL patterns under 'api/' path
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)