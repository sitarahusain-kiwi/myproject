"""
urls used for authentication app
"""
from django.urls import path, include

from apps.authentication import views
from apps.common.routers import OptionalSlashRouter

router = OptionalSlashRouter()
router.register(r'signup', views.SignUpViewSet, basename='signup')

urlpatterns = [
    path(r'auth/', include(router.urls)),
]
