"""
urls used for account app
"""
from django.urls import path, include

from apps.account import views
from apps.common.routers import OptionalSlashRouter

router = OptionalSlashRouter()
router.register(r'forgot-password', views.ForgotPasswordViewSet, basename='forgot_password')
router.register(r'verify-code', views.VerifyCodeViewSet, basename='verify_code')
router.register(r'set-password', views.SetPasswordViewSet, basename='set_password')

urlpatterns = [
    path(r'account/', include(router.urls)),
]
