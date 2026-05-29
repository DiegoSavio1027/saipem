from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    IncidentTrendViewSet,
    SafetyMetricsViewSet,
    ComplianceReportViewSet,
    LocationStatisticsViewSet
)

router = SimpleRouter(trailing_slash=True)
router.register(r'trends', IncidentTrendViewSet, basename='incident-trend')
router.register(r'metrics', SafetyMetricsViewSet, basename='safety-metrics')
router.register(r'compliance', ComplianceReportViewSet, basename='compliance-report')
router.register(r'locations', LocationStatisticsViewSet, basename='location-statistics')

urlpatterns = [
    path('', include(router.urls)),
]
