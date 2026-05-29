from django.contrib import admin
from .models import Vessel, Asset, MachineryEquipment, SparePart, WorkOrder, MaintenanceTask, InventoryItem


@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    list_display = ['id', 'vessel_name', 'vessel_type', 'imo_number', 'operational_status', 'health_score', 'last_inspected']
    list_filter = ['operational_status', 'vessel_type']
    search_fields = ['vessel_name', 'imo_number']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'last_inspected']


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_id', 'vessel', 'name', 'capacity', 'status', 'health_score', 'last_inspected']
    list_filter = ['status', 'vessel']
    search_fields = ['asset_id', 'name']
    ordering = ['-last_inspected']
    readonly_fields = ['last_inspected']


@admin.register(MachineryEquipment)
class MachineryEquipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'vessel', 'equipment_name', 'equipment_type', 'serial_number', 'operating_hours', 'needs_maintenance']
    list_filter = ['equipment_type', 'vessel']
    search_fields = ['equipment_name', 'serial_number']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ['id', 'vessel', 'part_name', 'part_number', 'quantity_on_hand', 'reorder_level', 'low_stock']
    list_filter = ['vessel', 'supplier']
    search_fields = ['part_name', 'part_number']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['wo_id', 'vessel', 'created_by', 'priority', 'scheduled_date', 'status', 'created_at']
    list_filter = ['status', 'priority', 'vessel', 'scheduled_date']
    search_fields = ['wo_id', 'description', 'created_by']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MaintenanceTask)
class MaintenanceTaskAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'vessel', 'equipment', 'wo_id', 'priority', 'scheduled_date', 'status', 'assigned_crew']
    list_filter = ['status', 'priority', 'vessel', 'scheduled_date']
    search_fields = ['task_id', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['item_code', 'item_name', 'category', 'current_stock', 'minimum_stock', 'asset_location']
    list_filter = ['category', 'asset_location']
    search_fields = ['item_code', 'item_name']
    ordering = ['item_name']
