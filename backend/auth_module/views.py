from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.conf import settings
import os
from .serializers import CustomTokenObtainPairSerializer, UserSerializer, get_user_role_and_modules


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT login endpoint that returns user info and role"""
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint that returns JWT tokens and user info
    POST /api/auth/login/
    Body: { "username": "user", "password": "pass" }
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.check_password(password):
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Generate tokens
    refresh = RefreshToken.for_user(user)

    # Get user role and accessible modules from Django Groups
    role, accessible_modules = get_user_role_and_modules(user)

    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_superuser': user.is_superuser,
            'role': role,
            'accessible_modules': accessible_modules
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    Get current user info
    GET /api/auth/me/
    Header: Authorization: Bearer <token>
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint (client-side token deletion)
    POST /api/auth/logout/
    """
    return Response(
        {'message': 'Logged out successfully'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def dev_quick_login_accounts(request):
    """
    Development-only endpoint that returns available test accounts
    Only available when DEBUG=True
    GET /api/v1/auth/dev/quick-login-accounts/
    """
    if not settings.DEBUG:
        return Response(
            {"error": "This endpoint is only available in development mode"},
            status=status.HTTP_403_FORBIDDEN
        )

    dev_enable = os.getenv('DEV_ENABLE_QUICK_LOGIN', 'False') == 'True'
    if not dev_enable:
        return Response(
            {"error": "Quick login is disabled"},
            status=status.HTTP_403_FORBIDDEN
        )

    accounts = {
        "admin": {
            "username": os.getenv('DEV_ADMIN_USERNAME', 'admin'),
            "password": os.getenv('DEV_ADMIN_PASSWORD', 'admin123'),
            "role": "Admin",
            "description": "Administrator account"
        },
        "hr_staff": {
            "username": os.getenv('DEV_HR_STAFF_USERNAME', 'hr_staff'),
            "password": os.getenv('DEV_HR_STAFF_PASSWORD', 'hr123'),
            "role": "HR Staff",
            "description": "HR Staff - HR Manager"
        },
        "safety_officer": {
            "username": os.getenv('DEV_SAFETY_OFFICER_USERNAME', 'safety_officer'),
            "password": os.getenv('DEV_SAFETY_OFFICER_PASSWORD', 'safety123'),
            "role": "Safety Officer",
            "description": "Safety Officer - HSE Officer"
        },
        "supervisor_engineer": {
            "username": os.getenv('DEV_SUPERVISOR_USERNAME', 'spv_engineer'),
            "password": os.getenv('DEV_SUPERVISOR_PASSWORD', 'spv123'),
            "role": "Supervisor Engineer",
            "description": "Supervisor Engineer - Engineering Supervisor"
        },
        "worker": {
            "username": os.getenv('DEV_WORKER_USERNAME', 'worker'),
            "password": os.getenv('DEV_WORKER_PASSWORD', 'worker123'),
            "role": "Worker",
            "description": "Field Worker - Mechanical Technician"
        }
    }

    return Response({
        "message": "Available test accounts for development",
        "accounts": accounts,
        "note": "These credentials are for development only"
    }, status=status.HTTP_200_OK)


from rest_framework import viewsets
from .serializers import UserManageSerializer
from .permissions import IsAdmin

class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD API for User management (Admin-only)
    """
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserManageSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

