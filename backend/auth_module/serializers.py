from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import UserProfile
import datetime


# Role to module access mapping
ROLE_MODULE_MAPPING = {
    'Admin': ['hr', 'asset', 'hse'],
    'HR Staff': ['hr'],
    'Chief Engineer': ['asset'],
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
            from hr_module.models import Employee, Roster
            import datetime
            
            # Find the Employee record linked by username
            employee = Employee.objects.filter(emp_id=obj.username).first()
            if not employee:
                return None
                
            # Find active roster for today
            today = datetime.date.today()
            active_roster = Roster.objects.filter(
                employee=employee,
                start_date__lte=today,
                end_date__gte=today
            ).first()
            
            if active_roster and active_roster.vessel:
                return {
                    'asset_id': active_roster.vessel.id,
                    'name': active_roster.vessel.vessel_name
                }
        except Exception:
            pass
        return None


class UserManageSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True, required=False)
    job_role = serializers.CharField(write_only=True, required=False)
    role_name = serializers.SerializerMethodField(read_only=True)
    job_role_name = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'job_role', 'role_name', 'job_role_name', 'password'
        ]

    def get_role_name(self, obj):
        role, _ = get_user_role_and_modules(obj)
        return role

    def get_job_role_name(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.job_role
        return ''

    def create(self, validated_data):
        role = validated_data.pop('role', 'Worker')
        job_role = validated_data.pop('job_role', 'Worker')
        password = validated_data.pop('password', None)

        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_password('saipem123')
        
        if role == 'Admin':
            user.is_superuser = True
            user.is_staff = True
        user.save()

        from django.contrib.auth.models import Group
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        if hasattr(user, 'profile'):
            user.profile.job_role = job_role
            user.profile.save()

        return user

    def update(self, instance, validated_data):
        role = validated_data.pop('role', None)
        job_role = validated_data.pop('job_role', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)

        if role:
            instance.groups.clear()
            from django.contrib.auth.models import Group
            group, _ = Group.objects.get_or_create(name=role)
            instance.groups.add(group)

            if role == 'Admin':
                instance.is_superuser = True
                instance.is_staff = True
            else:
                instance.is_superuser = False
                instance.is_staff = False
        
        instance.save()

        if job_role and hasattr(instance, 'profile'):
            instance.profile.job_role = job_role
            instance.profile.save()

        return instance

