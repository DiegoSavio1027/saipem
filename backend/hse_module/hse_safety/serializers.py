from rest_framework import serializers
from .models import Incident, StatusOverride, SystemStatus
from ..hse_pob.models import WorkLocation


class IncidentSerializer(serializers.ModelSerializer):
    """Serializer for Incident model"""

    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    impact = serializers.SerializerMethodField()
    reported_by_name = serializers.SerializerMethodField()
    proof_image = serializers.SerializerMethodField()

    class Meta:
        model = Incident
        fields = [
            'id',
            'incident_id',
            'severity',
            'severity_display',
            'location',
            'location_name',
            'vessel',
            'vessel_name',
            'description',
            'proof_image',
            'employee_name',
            'reported_by',
            'reported_by_name',
            'incident_date',
            'reported_date',
            'status',
            'status_display',
            'investigation_notes',
            'closed_by',
            'closed_date',
            'created_at',
            'updated_at',
            'impact'
        ]
        read_only_fields = ['id', 'incident_id', 'reported_date', 'created_at', 'updated_at', 'vessel_name']

    def get_impact(self, obj):
        """Return impact dari incident terhadap metrics"""
        return obj.get_impact_on_metrics()

    def get_reported_by_name(self, obj):
        """Get reporter's full name from Employee model"""
        if not obj.reported_by:
            return "Unknown"

        from ..hse_ptw.models import Employee
        try:
            employee = Employee.objects.get(emp_id=obj.reported_by)
            return employee.full_name
        except Employee.DoesNotExist:
            return obj.reported_by

    def get_proof_image(self, obj):
        """Return full URL for proof image"""
        if obj.proof_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.proof_image.url)
            return obj.proof_image.url
        return None


class StatusOverrideSerializer(serializers.ModelSerializer):
    """Serializer untuk StatusOverride model"""

    previous_status_display = serializers.CharField(source='get_previous_status_display', read_only=True)
    new_status_display = serializers.CharField(source='get_new_status_display', read_only=True)

    class Meta:
        model = StatusOverride
        fields = [
            'id',
            'previous_status',
            'previous_status_display',
            'new_status',
            'new_status_display',
            'override_reason',
            'changed_by',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class StatusOverrideDetailedSerializer(serializers.ModelSerializer):
    """Enhanced serializer untuk StatusOverride dengan employee details"""

    previous_status_display = serializers.CharField(source='get_previous_status_display', read_only=True)
    new_status_display = serializers.CharField(source='get_new_status_display', read_only=True)
    changed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = StatusOverride
        fields = [
            'id',
            'previous_status',
            'previous_status_display',
            'new_status',
            'new_status_display',
            'override_reason',
            'changed_by',
            'changed_by_name',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_changed_by_name(self, obj):
        """Get employee full name from Employee model"""
        if not obj.changed_by:
            return "Unknown"

        from ..hse_ptw.models import Employee
        try:
            employee = Employee.objects.get(emp_id=obj.changed_by)
            return employee.full_name
        except Employee.DoesNotExist:
            return obj.changed_by


class SystemStatusSerializer(serializers.ModelSerializer):
    """Serializer untuk SystemStatus model"""

    global_status_display = serializers.CharField(source='get_global_status_display', read_only=True)

    class Meta:
        model = SystemStatus
        fields = [
            'id',
            'global_status',
            'global_status_display',
            'days_without_lti',
            'last_lti_date',
            'near_misses_count',
            'active_permits',
            'updated_at',
            'last_incident_date'
        ]
        read_only_fields = ['id', 'updated_at']


class IncidentReportSerializer(serializers.Serializer):
    """Serializer untuk menerima incident report dari frontend"""

    severity = serializers.ChoiceField(
        choices=['SAFETY_OBSERVATION', 'NEAR_MISS', 'FIRST_AID', 'LTI']
    )
    location = serializers.IntegerField()
    description = serializers.CharField(max_length=1000)
    employee_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    reported_by = serializers.CharField(max_length=50)
    incident_date = serializers.DateTimeField()
    proof_image = serializers.ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        """Create incident dan update system status"""
        location_id = validated_data.pop('location')
        location = WorkLocation.objects.get(id=location_id)
        validated_data['location'] = location

        # Determine initial status based on reporter role
        from ..hse_ptw.models import Employee
        reporter_emp_id = validated_data.get('reported_by')
        initial_status = 'OPEN'

        try:
            employee = Employee.objects.get(emp_id=reporter_emp_id)
            if employee.job_role == 'Worker':
                initial_status = 'PENDING_VERIFICATION'
        except Employee.DoesNotExist:
            pass

        validated_data['status'] = initial_status
        incident = Incident.objects.create(**validated_data)

        # Only update system status if incident is verified (not pending)
        if initial_status != 'PENDING_VERIFICATION':
            system_status, _ = SystemStatus.get_or_create_singleton()
            impact = incident.get_impact_on_metrics()

            # Update metrics berdasarkan impact
            if impact['days_without_lti'] == 'RESET_TO_ZERO':
                system_status.days_without_lti = 0
                system_status.last_lti_date = incident.incident_date.date()

            if impact['near_misses'] == 'INCREMENT':
                system_status.near_misses_count += 1

            if impact['global_status'] != 'NO_CHANGE':
                system_status.global_status = impact['global_status']

            system_status.last_incident_date = incident.incident_date
            system_status.save()

        return incident


class StatusOverrideRequestSerializer(serializers.Serializer):
    """Serializer untuk menerima manual status override request"""

    status = serializers.ChoiceField(choices=['GREEN', 'YELLOW', 'RED'])
    override_reason = serializers.CharField(max_length=500, min_length=10, required=True)

    def validate_override_reason(self, value):
        """Validate that override_reason is not empty or just whitespace"""
        if not value or not value.strip():
            raise serializers.ValidationError("Override reason cannot be empty")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Override reason must be at least 10 characters")
        return value.strip()

    def create(self, validated_data):
        """Create status override dan update system status"""
        system_status, _ = SystemStatus.get_or_create_singleton()

        # Create override record (audit trail)
        override = StatusOverride.objects.create(
            previous_status=system_status.global_status,
            new_status=validated_data['status'],
            override_reason=validated_data['override_reason'],
            changed_by=self.context.get('user_id', 'UNKNOWN')
        )

        # Update system status
        system_status.global_status = validated_data['status']
        system_status.save()

        return override
