from rest_framework import serializers
from .models import PermitToWork, Employee
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
    employee = serializers.SerializerMethodField()
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
                'created_at': work_order.created_at
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

    class Meta:
        model = PermitToWork
        fields = [
            'id', 'permit_id', 'emp_id', 'wo_id', 'deck_location', 'vessel', 'vessel_name', 'permit_type', 'permit_type_display',
            'status', 'status_display', 'approved_by', 'approved_by_name', 'approved_at', 'signature',
            'rejected_by', 'rejected_by_name', 'rejected_at', 'rejection_reason', 'completion_notes',
            'closed_by', 'closed_by_name', 'closed_at', 'closing_notes', 'created_at', 'updated_at',
            'employee', 'work_order'
        ]
        read_only_fields = ['id', 'permit_id', 'created_at', 'updated_at', 'vessel_name']