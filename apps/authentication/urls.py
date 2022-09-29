"""
urls used for authentication app
"""
from django.urls import path, include

from apps.authentication import views
from apps.common.routers import OptionalSlashRouter

router = OptionalSlashRouter()
router.register(r'signup', views.SignUpViewSet, basename='signup')
router.register(r'verification', views.AccountOtpVerificationViewSet, basename='verification')
router.register(r'login', views.LoginViewSet, basename='login')
router.register(r'logout', views.LogoutViewSet, basename='logout')

urlpatterns = [
    path(r'auth/', include(router.urls)),
]
