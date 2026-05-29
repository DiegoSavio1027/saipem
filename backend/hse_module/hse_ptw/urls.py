from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import EmployeeViewSet, PermitToWorkViewSet

# Use SimpleRouter with trailing_slash=True to match frontend requests
router = SimpleRouter(trailing_slash=True)
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'ptw', PermitToWorkViewSet, basename='ptw')

urlpatterns = [
    path('', include(router.urls)),
]
