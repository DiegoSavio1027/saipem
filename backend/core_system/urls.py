from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from hse_module.hse_pob.views import pob_dashboard
from .views import api_root, api_v1_root

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Root
    path('api/', api_root, name='api_root'),
    path('api/v1/', api_v1_root, name='api_v1_root'),

    # Auth
    path('api/v1/auth/', include('auth_module.urls')),

    # Offshore (Vessel & Location/Deck Management)
    path('api/v1/offshore/', include('offshore_module.urls')),

    # HSE (includes test-trigger and all HSE modules)
    path('api/v1/hse/', include('hse_module.urls')),

    # HR
    path('api/v1/hr/', include('hr_module.urls')),

    # Asset
    path('api/v1/asset/', include('asset_module.urls')),

    # Dashboard
    path('dashboard/', pob_dashboard, name='pob_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
