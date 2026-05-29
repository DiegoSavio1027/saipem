from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import IncidentViewSet, SystemStatusViewSet

router = SimpleRouter(trailing_slash=True)
router.register(r'incidents', IncidentViewSet, basename='incident')
router.register(r'status', SystemStatusViewSet, basename='system-status')

urlpatterns = [
    path('', include(router.urls)),
]
