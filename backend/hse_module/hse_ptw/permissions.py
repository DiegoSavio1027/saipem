from rest_framework import permissions


class IsHRStaffOrAdmin(permissions.BasePermission):
    """
    Permission class: Allow HR Staff and Admin to perform actions
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Admin/superuser always allowed
        if request.user.is_superuser:
            return True

        # Check if user is in HR Staff or Admin group
        return request.user.groups.filter(name__in=['HR Staff', 'Admin']).exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission class: Allow users to only view/edit their own Employee record
    Workers can only see their own data
    """
    def has_object_permission(self, request, view, obj):
        # Admin and HR Staff can access all
        if request.user.is_superuser:
            return True

        if request.user.groups.filter(name__in=['HR Staff', 'Admin', 'Safety Officer']).exists():
            return True

        # Workers can only access their own record
        return obj.emp_id == request.user.username


class IsSafetyOfficerOrAdmin(permissions.BasePermission):
    """
    Permission class: Allow Safety Officer and Admin
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return request.user.groups.filter(name__in=['Safety Officer', 'Admin']).exists()
