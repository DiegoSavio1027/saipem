from rest_framework import serializers
from .models import (
    Vessel,
    Asset,
    MachineryEquipment,
    SparePart,
    WorkOrder,
    MaintenanceTask,
    InventoryItem
)


# ==========================================
# VESSEL SERIALIZER
# ==========================================
class VesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vessel
        fields = '__all__'


# ==========================================
# ASSET SERIALIZER
# ==========================================
class AssetSerializer(serializers.ModelSerializer):
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)

    class Meta:
        model = Asset
        fields = '__all__'


# ==========================================
# MACHINERY EQUIPMENT SERIALIZER
# ==========================================
class MachineryEquipmentSerializer(serializers.ModelSerializer):
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)
    hours_until_maintenance = serializers.IntegerField(read_only=True)
    needs_maintenance = serializers.BooleanField(read_only=True)

    class Meta:
        model = MachineryEquipment
        fields = '__all__'


# ==========================================
# SPARE PART SERIALIZER
# ==========================================
class SparePartSerializer(serializers.ModelSerializer):
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)
    low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = SparePart
        fields = '__all__'


# ==========================================
# WORK ORDER SERIALIZER
# ==========================================
class WorkOrderSerializer(serializers.ModelSerializer):
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)

    class Meta:
        model = WorkOrder
        fields = '__all__'


# ==========================================
# MAINTENANCE TASK SERIALIZER
# ==========================================
class MaintenanceTaskSerializer(serializers.ModelSerializer):
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)
    equipment_name = serializers.CharField(source='equipment.equipment_name', read_only=True, allow_null=True)
    crew_name = serializers.CharField(source='assigned_crew.full_name', read_only=True, allow_null=True)
    wo_number = serializers.CharField(source='wo_id.wo_id', read_only=True, allow_null=True)

    class Meta:
        model = MaintenanceTask
        fields = '__all__'


# ==========================================
# INVENTORY ITEM SERIALIZER
# ==========================================
class InventoryItemSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset_location.name', read_only=True, allow_null=True)
    vessel_name = serializers.CharField(source='asset_location.vessel.vessel_name', read_only=True, allow_null=True)
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItem
        fields = '__all__'

    def get_is_low_stock(self, obj):
        return obj.current_stock <= obj.minimum_stock
