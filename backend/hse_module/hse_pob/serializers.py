from rest_framework import serializers
from .models import WorkLocation, POBLog

class WorkLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkLocation
        fields = ['id', 'deck_name', 'risk_level']

class VesselWithDecksSerializer(serializers.Serializer):
    """Serializer untuk vessel dengan assigned decks"""
    vessel_id = serializers.IntegerField(source='id')
    vessel_name = serializers.CharField()
    vessel_type = serializers.CharField()
    operational_status = serializers.CharField()
    assigned_decks = serializers.SerializerMethodField()

    def get_assigned_decks(self, obj):
        # Get assigned decks from the many-to-many relationship
        decks = obj.assigned_decks.all().values('id', 'deck_name', 'risk_level')
        return list(decks)

class POBLogSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)

    def get_employee_name(self, obj):
        from ..hse_ptw.models import Employee
        try:
            employee = Employee.objects.get(emp_id=obj.emp_id)
            return employee.full_name
        except Employee.DoesNotExist:
            return obj.emp_id

    class Meta:
        model = POBLog
        fields = ['id', 'emp_id', 'employee_name', 'deck_location', 'vessel', 'vessel_name', 'action', 'timestamp']
        read_only_fields = ['timestamp', 'vessel_name']

