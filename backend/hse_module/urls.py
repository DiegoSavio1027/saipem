from django.urls import path, include
from hse_module.hse_pob.views import test_trigger

urlpatterns = [
    # PTW (Permit to Work)
    path('', include('hse_module.hse_ptw.urls')),

    # POB (Personnel on Board)
    path('', include('hse_module.hse_pob.urls')),

    # Safety (Incidents & System Status)
    path('', include('hse_module.hse_safety.urls')),

    # Analytics
    path('analytics/', include('hse_module.hse_analytics.urls')),

    # Test trigger
    path('test-trigger/', test_trigger, name='test_trigger'),
]
