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
from hse_module.hse_pob.models import WorkLocation


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
    vibration = serializers.SerializerMethodField()
    temperature = serializers.SerializerMethodField()
    rul_hours = serializers.SerializerMethodField()
    predicted_failure_date = serializers.SerializerMethodField()
    assigned_decks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=WorkLocation.objects.all(),
        required=False
    )

    class Meta:
        model = Asset
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['assigned_decks_details'] = [
            {'id': deck.id, 'deck_name': deck.deck_name, 'risk_level': deck.risk_level}
            for deck in instance.assigned_decks.all()
        ]
        return representation


    def get_vibration(self, obj):
        import random
        from django.utils import timezone
        # Use simple seed based on asset name length and ID
        state_seed = len(obj.name) + int(timezone.now().timestamp() // 15) % 100
        random.seed(state_seed)
        if obj.status == 'CRITICAL':
            return round(random.uniform(7.0, 9.8), 2)
        elif obj.status == 'MAINTENANCE':
            return round(random.uniform(4.0, 6.0), 2)
        return round(random.uniform(1.0, 3.2), 2)

    def get_temperature(self, obj):
        import random
        from django.utils import timezone
        state_seed = len(obj.name) + 20 + int(timezone.now().timestamp() // 15) % 100
        random.seed(state_seed)
        if obj.status == 'CRITICAL':
            return round(random.uniform(85.0, 105.0), 1)
        elif obj.status == 'MAINTENANCE':
            return round(random.uniform(65.0, 78.0), 1)
        return round(random.uniform(35.0, 55.0), 1)

    def get_rul_hours(self, obj):
        if obj.status == 'CRITICAL':
            return 12
        elif obj.status == 'MAINTENANCE':
            return 150
        return 850

    def get_predicted_failure_date(self, obj):
        import datetime
        from django.utils import timezone
        rul_days = self.get_rul_hours(obj) / 24.0
        predicted_date = timezone.now().date() + datetime.timedelta(days=rul_days)
        return predicted_date.isoformat()


# ==========================================
# MACHINERY EQUIPMENT SERIALIZER
# ==========================================
class MachineryEquipmentSerializer(serializers.ModelSerializer):
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)
    hours_until_maintenance = serializers.IntegerField(read_only=True)
    needs_maintenance = serializers.BooleanField(read_only=True)
    vibration = serializers.SerializerMethodField()
    temperature = serializers.SerializerMethodField()
    rul_hours = serializers.SerializerMethodField()
    predicted_failure_date = serializers.SerializerMethodField()
    health_percentage = serializers.SerializerMethodField()

    class Meta:
        model = MachineryEquipment
        fields = '__all__'

    def get_vibration(self, obj):
        import random
        from django.utils import timezone
        # Seed by id to make it stable but add a small fluctuation
        state_seed = obj.id + int(timezone.now().timestamp() // 10) % 100
        random.seed(state_seed)
        
        if obj.needs_maintenance:
            # High vibration when needs maintenance
            return round(random.uniform(6.5, 9.2), 2)
        else:
            # Normal vibration
            return round(random.uniform(1.2, 3.8), 2)

    def get_temperature(self, obj):
        import random
        from django.utils import timezone
        state_seed = obj.id + 10 + int(timezone.now().timestamp() // 10) % 100
        random.seed(state_seed)
        
        if obj.needs_maintenance:
            # High temperature when needs maintenance
            return round(random.uniform(78.0, 94.5), 1)
        else:
            # Normal temperature
            return round(random.uniform(42.0, 68.5), 1)

    def get_rul_hours(self, obj):
        return obj.hours_until_maintenance

    def get_predicted_failure_date(self, obj):
        import datetime
        from django.utils import timezone
        
        rul_days = obj.hours_until_maintenance / 24.0
        predicted_date = timezone.now().date() + datetime.timedelta(days=rul_days)
        return predicted_date.isoformat()

    def get_health_percentage(self, obj):
        if obj.needs_maintenance:
            return 25  # critical warning health
        
        total = obj.maintenance_interval_hours
        remaining = obj.hours_until_maintenance
        if total <= 0:
            return 100
        return max(30, int((remaining / total) * 100))


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
    asset_name = serializers.CharField(source='asset.name', read_only=True, allow_null=True)
    machinery_name = serializers.CharField(source='machinery.equipment_name', read_only=True, allow_null=True)
    asset_assigned_decks = serializers.SerializerMethodField()

    class Meta:
        model = WorkOrder
        fields = '__all__'

    def get_asset_assigned_decks(self, obj):
        if obj.asset:
            return [
                {'id': deck.id, 'deck_name': deck.deck_name, 'risk_level': deck.risk_level}
                for deck in obj.asset.assigned_decks.all()
            ]
        return []


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
