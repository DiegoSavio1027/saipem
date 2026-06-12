from rest_framework import serializers
from .models import PermitToWork
from hr_module.models import Employee
from asset_module.models import WorkOrder


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, help_text="Password for User account (auto-generated if not provided)")

    class Meta:
        model = Employee
        fields = ['emp_id', 'full_name', 'job_role', 'roster_status', 'email', 'mcu_expiry', 'mcu_status', 'created_at', 'password']
        read_only_fields = ['created_at', 'mcu_status']
        extra_kwargs = {
            'email': {'required': False},
            'mcu_expiry': {'required': False},
        }


class PermitToWorkSerializer(serializers.ModelSerializer):
    permit_type_display = serializers.CharField(source='get_permit_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)
    deck_location_name = serializers.CharField(source='deck_location.deck_name', read_only=True)
    employee = serializers.SerializerMethodField()
    assigned_crew = serializers.SerializerMethodField()
    assigned_personnel_ids = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    work_order = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()
    closed_by_name = serializers.SerializerMethodField()
    rejected_by_name = serializers.SerializerMethodField()

    def get_employee(self, obj):
        emp_id = obj.get('emp_id') if isinstance(obj, dict) else obj.emp_id
        if not emp_id:
            return None
        try:
            employee = Employee.objects.get(emp_id=emp_id)
            return EmployeeSerializer(employee).data
        except Employee.DoesNotExist:
            return None

    def get_assigned_crew(self, obj):
        crew = getattr(obj, 'assigned_personnel', None)
        if crew:
            return EmployeeSerializer(crew.all(), many=True).data
        return []

    def get_work_order(self, obj):
        wo_id = obj.get('wo_id') if isinstance(obj, dict) else obj.wo_id
        if not wo_id:
            return None
        try:
            work_order = WorkOrder.objects.get(wo_id=wo_id)
            return {
                'wo_id': work_order.wo_id,
                'description': work_order.description,
                'scheduled_date': work_order.scheduled_date,
                'status': work_order.status,
                'created_at': work_order.created_at,
                'target_asset': work_order.asset.name if work_order.asset else (work_order.machinery.equipment_name if work_order.machinery else '-'),
                'asset_assigned_decks': [
                    {'id': deck.id, 'deck_name': deck.deck_name, 'risk_level': deck.risk_level}
                    for deck in work_order.asset.assigned_decks.all()
                ] if work_order.asset else []
            }
        except WorkOrder.DoesNotExist:
            return None

    def get_approved_by_name(self, obj):
        approved_by = obj.get('approved_by') if isinstance(obj, dict) else obj.approved_by
        if not approved_by:
            return None
        try:
            employee = Employee.objects.get(emp_id=approved_by)
            return employee.full_name
        except Employee.DoesNotExist:
            return approved_by

    def get_closed_by_name(self, obj):
        closed_by = obj.get('closed_by') if isinstance(obj, dict) else obj.closed_by
        if not closed_by:
            return None
        try:
            employee = Employee.objects.get(emp_id=closed_by)
            return employee.full_name
        except Employee.DoesNotExist:
            return closed_by

    def get_rejected_by_name(self, obj):
        rejected_by = obj.get('rejected_by') if isinstance(obj, dict) else obj.rejected_by
        if not rejected_by:
            return None
        try:
            employee = Employee.objects.get(emp_id=rejected_by)
            return employee.full_name
        except Employee.DoesNotExist:
            return rejected_by

    def validate(self, data):
        instance = self.instance
        emp_id = data.get('emp_id') or (instance.emp_id if instance else None)
        permit_type = data.get('permit_type') or (instance.permit_type if instance else None)
        vessel = data.get('vessel') or (instance.vessel if instance else None)
        wo_id = data.get('wo_id') or (instance.wo_id if instance else None)
        deck_location = data.get('deck_location') or (instance.deck_location if instance else None)

        if emp_id:
            try:
                employee = Employee.objects.get(emp_id=emp_id)
                from datetime import date
                today = date.today()

                # Phase 4 Interlock: Roster Validation
                from hr_module.models import Roster
                if vessel:
                    is_onboard = Roster.objects.filter(
                        employee=employee,
                        vessel=vessel,
                        start_date__lte=today,
                        end_date__gte=today
                    ).exists()
                    if not is_onboard:
                        raise serializers.ValidationError({"emp_id": f"Employee is not rostered on vessel {vessel.vessel_name} today."})

                # Phase 4 Interlock: Asset Validation
                if wo_id and vessel and wo_id.vessel != vessel:
                    raise serializers.ValidationError({"wo_id": "Work Order does not belong to the selected vessel."})

                # Phase 4 Interlock: Location Validation
                if deck_location and vessel:
                    if not vessel.assigned_decks.filter(id=deck_location.id).exists():
                        raise serializers.ValidationError({"deck_location": "Location is not assigned to the selected vessel."})

                # Phase 4 Interlock: Asset Deck Location Validation
                if wo_id and wo_id.asset and deck_location:
                    asset = wo_id.asset
                    if not asset.assigned_decks.filter(id=deck_location.id).exists():
                        valid_decks = ", ".join(d.deck_name for d in asset.assigned_decks.all())
                        raise serializers.ValidationError({
                            "deck_location": f"Selected location is not valid for asset '{asset.name}' (must be one of: {valid_decks})."
                        })

                # Gatekeeper: Medical Status
                if not instance or data.get('emp_id'):
                    if employee.mcu_status != 'FIT':
                        raise serializers.ValidationError({"emp_id": "Employee must be medically FIT to create a PTW."})

                # Gatekeeper: Certifications
                if not instance or data.get('permit_type') or data.get('emp_id'):
                    from hr_module.models import Certification
                    
                    has_valid_cert = Certification.objects.filter(
                        employee=employee,
                        cert_type=permit_type,
                        expiry_date__gte=today
                    ).exists()
                    
                    if not has_valid_cert:
                        raise serializers.ValidationError({"permit_type": f"Employee does not have a valid {permit_type} certification."})
            except Employee.DoesNotExist:
                raise serializers.ValidationError({"emp_id": "Employee not found."})
        return data

    class Meta:
        model = PermitToWork
        fields = [
            'id', 'permit_id', 'emp_id', 'wo_id', 'deck_location', 'deck_location_name', 'vessel', 'vessel_name', 'permit_type', 'permit_type_display',
            'status', 'status_display', 'approved_by', 'approved_by_name', 'approved_at', 'signature',
            'rejected_by', 'rejected_by_name', 'rejected_at', 'rejection_reason', 'completion_notes',
            'is_toolbox_talk_done', 'closed_by', 'closed_by_name', 'closed_at', 'closing_notes', 'created_at', 'updated_at',
            'employee', 'work_order', 'assigned_crew', 'assigned_personnel_ids'
        ]
        read_only_fields = ['id', 'permit_id', 'created_at', 'updated_at', 'vessel_name', 'deck_location_name']

    def create(self, validated_data):
        assigned_ids = validated_data.pop('assigned_personnel_ids', [])
        ptw = super().create(validated_data)
        if assigned_ids:
            employees = Employee.objects.filter(emp_id__in=assigned_ids)
            ptw.assigned_personnel.set(employees)
        return ptw