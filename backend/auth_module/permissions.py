from rest_framework import permissions


# Role to module access mapping
ROLE_MODULE_MAPPING = {
    'Admin': ['hr', 'asset', 'hse'],
    'HR Staff': ['hr'],
    'Chief Engineer': ['asset'],
    'Worker': ['hse'],
    'Safety Officer': ['hse'],
}


def get_user_accessible_modules(user):
    """Get user's accessible modules from Django Groups"""
    if user.is_superuser:
        return ['hr', 'asset', 'hse']

    if user.groups.exists():
        group_name = user.groups.first().name
        return ROLE_MODULE_MAPPING.get(group_name, ['hse'])

    return ['hse']


class HasModuleAccess(permissions.BasePermission):
    """
    Permission class to check if user has access to specific module
    Usage: permission_classes = [HasModuleAccess]
    Set required_module in view: required_module = 'hr' or 'asset' or 'hse'
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Admin has access to everything
        if request.user.is_superuser:
            return True

        # Get required module from view
        required_module = getattr(view, 'required_module', None)
        if not required_module:
            return True  # No module restriction

        # Check user's accessible modules
        accessible_modules = get_user_accessible_modules(request.user)
        return required_module in accessible_modules


class IsHRStaff(permissions.BasePermission):
    """Permission for HR module access"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        accessible_modules = get_user_accessible_modules(request.user)
        return 'hr' in accessible_modules


class IsAssetStaff(permissions.BasePermission):
    """Permission for Asset module access"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        accessible_modules = get_user_accessible_modules(request.user)
        return 'asset' in accessible_modules


class IsHSEStaff(permissions.BasePermission):
    """Permission for HSE module access"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        accessible_modules = get_user_accessible_modules(request.user)
        return 'hse' in accessible_modules


class IsAdmin(permissions.BasePermission):
    """Permission for Admin-only operations"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Admin').exists()

