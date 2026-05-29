from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API Root - Menampilkan daftar endpoint yang tersedia
    """
    return JsonResponse({
        'message': 'Saipem HSE Management System API',
        'version': 'v1',
        'endpoints': {
            'authentication': {
                'login': '/api/v1/auth/login/',
                'logout': '/api/v1/auth/logout/',
                'me': '/api/v1/auth/me/',
                'jwt_token': '/api/v1/auth/token/',
                'jwt_refresh': '/api/v1/auth/token/refresh/',
            },
            'hse': {
                'locations': '/api/v1/hse/locations/',
                'pob': '/api/v1/hse/pob/',
                'ptw': '/api/v1/hse/ptw/',
                'incidents': '/api/v1/hse/incidents/',
                'analytics': '/api/v1/hse/analytics/',
            },
            'hr': {
                'employees': '/api/v1/hr/employees/',
                'rosters': '/api/v1/hr/rosters/',
                'assets': '/api/v1/hr/assets/',
                'activities': '/api/v1/hr/activities/',
                'payroll': '/api/v1/hr/payroll/',
                'analytics': '/api/v1/hr/analytics/',
                'positions': '/api/v1/hr/positions/',
            },
            'asset': {
                'maintenance': '/api/v1/asset/maintenance/',
                'inventory': '/api/v1/asset/inventory/',
            },
            'admin': '/admin/',
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_v1_root(request):
    """
    API v1 Root - Menampilkan daftar modul yang tersedia di v1
    """
    return JsonResponse({
        'message': 'Saipem HSE API v1',
        'modules': {
            'auth': '/api/v1/auth/',
            'hse': '/api/v1/hse/',
            'hr': '/api/v1/hr/',
            'asset': '/api/v1/asset/',
        },
        'documentation': 'Contact admin for API documentation'
    })
