from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import UserProfile
import datetime


# Role to module access mapping
ROLE_MODULE_MAPPING = {
    'Admin': ['hr', 'asset', 'hse'],
    'HR Staff': ['hr'],
    'Supervisor Engineer': ['asset'],
    'Worker': ['hse'],
    'Safety Officer': ['hse'],
}


def get_user_role_and_modules(user):
    """Get user's role and accessible modules from Django Groups"""
    if user.is_superuser:
        return 'Admin', ['hr', 'asset', 'hse']

    if user.groups.exists():
        group_name = user.groups.first().name
        accessible_modules = ROLE_MODULE_MAPPING.get(group_name, ['hse'])
        return group_name, accessible_modules

    return 'Worker', ['hse']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""

    class Meta:
        model = UserProfile
        fields = ['job_role', 'roster_status', 'mcu_expiry', 'mcu_status', 'created_at']
        read_only_fields = ['created_at']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT serializer that includes user info and role"""

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Use UserSerializer to include assigned_vessel
        serializer = UserSerializer(user)
        data['user'] = serializer.data

        return data


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    accessible_modules = serializers.SerializerMethodField()
    assigned_vessel = serializers.SerializerMethodField()
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'role', 'accessible_modules', 'assigned_vessel', 'profile']

    def get_role(self, obj):
        role, _ = get_user_role_and_modules(obj)
        return role

    def get_accessible_modules(self, obj):
        _, accessible_modules = get_user_role_and_modules(obj)
        return accessible_modules

    def get_assigned_vessel(self, obj):
        """Fetch user's currently assigned vessel from active roster"""
        try:
            today = datetime.date.today()
            # For now, return None since we're transitioning from Employee to User model
            # TODO: Update Roster model to reference User instead of Employee
            return None
        except Exception:
            pass
        return None
