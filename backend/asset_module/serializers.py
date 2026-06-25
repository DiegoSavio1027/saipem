from rest_framework import serializers
from .models import (
    Vessel,
    Asset,
    MachineryEquipment,
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
    vibration = serializers.DecimalField(source='current_vibration', max_digits=5, decimal_places=2, read_only=True)
    temperature = serializers.DecimalField(source='current_temperature', max_digits=5, decimal_places=2, read_only=True)
    machinery_count = serializers.IntegerField(source='machinery_equipment.count', read_only=True)
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
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    hours_until_maintenance = serializers.IntegerField(read_only=True)
    needs_maintenance = serializers.BooleanField(read_only=True)
    vibration = serializers.DecimalField(source='current_vibration', max_digits=5, decimal_places=2, read_only=True)
    temperature = serializers.DecimalField(source='current_temperature', max_digits=5, decimal_places=2, read_only=True)
    rul_hours = serializers.SerializerMethodField()
    predicted_failure_date = serializers.SerializerMethodField()
    health_percentage = serializers.SerializerMethodField()

    class Meta:
        model = MachineryEquipment
        fields = '__all__'


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



from .models import WorkOrderMaterial

class WorkOrderMaterialSerializer(serializers.ModelSerializer):
    part_name = serializers.CharField(source='inventory_item.item_name', read_only=True)
    part_number = serializers.CharField(source='inventory_item.item_code', read_only=True)

    class Meta:
        model = WorkOrderMaterial
        fields = ['id', 'inventory_item', 'part_name', 'part_number', 'quantity_used', 'added_at']


# ==========================================
# WORK ORDER SERIALIZER
# ==========================================
class WorkOrderSerializer(serializers.ModelSerializer):
    vessel_name = serializers.CharField(source='vessel.vessel_name', read_only=True)
    asset_name = serializers.CharField(source='asset.name', read_only=True, allow_null=True)
    machinery_name = serializers.CharField(source='machinery.equipment_name', read_only=True, allow_null=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True, allow_null=True)
    asset_assigned_decks = serializers.SerializerMethodField()
    materials = WorkOrderMaterialSerializer(many=True, read_only=True)

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

    def validate(self, data):
        assigned_to = data.get('assigned_to', None)
        scheduled_date = data.get('scheduled_date', None)
        status = data.get('status', 'PENDING')
        
        # If updating, merge with instance data
        if self.instance:
            assigned_to = assigned_to or self.instance.assigned_to
            scheduled_date = scheduled_date or self.instance.scheduled_date
            
        # We only apply the limit check if assigning a pending/in_progress work order
        if assigned_to and scheduled_date and status in ['PENDING', 'IN_PROGRESS']:
            active_wos = WorkOrder.objects.filter(
                assigned_to=assigned_to,
                scheduled_date=scheduled_date,
                status__in=['PENDING', 'IN_PROGRESS']
            )
            
            if self.instance:
                active_wos = active_wos.exclude(pk=self.instance.pk)
                
            if active_wos.exists():
                raise serializers.ValidationError({
                    "assigned_to": f"Employee {assigned_to.full_name} already has an active task assigned on {scheduled_date}. Please select another date or another employee."
                })
                
        return data


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
    vessel_name = serializers.SerializerMethodField()
    low_stock = serializers.BooleanField(read_only=True)
    available_stock = serializers.IntegerField(read_only=True)

    class Meta:
        model = InventoryItem
        fields = '__all__'

    def get_vessel_name(self, obj):
        if obj.vessel:
            return obj.vessel.vessel_name
        if obj.asset_location and obj.asset_location.vessel:
            return obj.asset_location.vessel.vessel_name
        return None
