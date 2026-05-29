import datetime
from rest_framework import serializers
from hse_module.hse_ptw.models import Employee
from .models import Roster, VesselActivity, Position

# ==========================================
# 1. EMPLOYEE SERIALIZER
# ==========================================
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


# ==========================================
# 2. ROSTER SCHEDULING SERIALIZER (WITH MCU BLOCKER!)
# ==========================================
class RosterSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='employee.full_name', read_only=True)
    start = serializers.DateField(source='start_date')
    end = serializers.DateField(source='end_date')
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)

    class Meta:
        model = Roster
        fields = ['id', 'employee', 'title', 'start', 'end', 'vessel', 'vessel_name', 'location']

    # --- SMART BACKEND BLOCKER (Failsafe Security) ---
    def validate(self, data):
        employee = data.get('employee')
        if employee:
            # A. Cek status medis UNFIT
            if employee.mcu_status == 'UNFIT':
                raise serializers.ValidationError(
                    f"DEPLOYMENT DENIED: Personnel {employee.full_name} is medically UNFIT."
                )
            # B. Cek status medis EXPIRED di database
            if employee.mcu_status == 'EXPIRED':
                raise serializers.ValidationError(
                    f"DEPLOYMENT DENIED: Personnel {employee.full_name} MCU has EXPIRED."
                )

            # C. Auto-check tanggal kadaluarsa MCU melewati hari ini
            today = datetime.date.today()
            if employee.mcu_expiry and employee.mcu_expiry < today:
                raise serializers.ValidationError(
                    f"DEPLOYMENT DENIED: Personnel {employee.full_name} MCU expired on {employee.mcu_expiry}."
                )
                
        return data

    def create(self, validated_data):
        return super().create(validated_data)


# ==========================================
# 3. VESSEL ACTIVITY SERIALIZER
# ==========================================
class VesselActivitySerializer(serializers.ModelSerializer):
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)
    start = serializers.DateField(source='start_date')
    end = serializers.DateField(source='end_date')
    
    class Meta:
        model = VesselActivity
        fields = ['id', 'asset', 'asset_name', 'start', 'end', 'activity_name']


# ==========================================
# 5. POSITION RATE SERIALIZER
# ==========================================
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'