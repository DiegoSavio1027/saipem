from django.db import models
from django.utils import timezone

# ==========================================
# VESSEL MODEL (Multi-vessel support)
# ==========================================
class Vessel(models.Model):
    """Vessel/Kapal information"""
    OPERATIONAL_STATUS_CHOICES = [
        ('OPERATIONAL', 'Operational'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('CRITICAL', 'Critical'),
        ('INACTIVE', 'Inactive'),
    ]

    id = models.AutoField(primary_key=True)
    vessel_name = models.CharField(max_length=100, unique=True)
    vessel_type = models.CharField(max_length=100)  # ex: Drill Ship, FPSO, Supply Vessel
    imo_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    operational_status = models.CharField(max_length=50, choices=OPERATIONAL_STATUS_CHOICES, default='OPERATIONAL')
    health_score = models.IntegerField(default=100)  # 0-100%
    last_inspected = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_decks = models.ManyToManyField('hse_pob.WorkLocation', related_name='vessels', blank=True)

    def __str__(self):
        return self.vessel_name


# ==========================================
# ASSET MODEL (Moved from hr_module)
# ==========================================
class Asset(models.Model):
    """Asset/Equipment on vessel"""
    STATUS_CHOICES = [
        ('OPERATIONAL', 'Operational'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('CRITICAL', 'Critical'),
    ]

    asset_id = models.CharField(max_length=50, primary_key=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=100)
    capacity = models.CharField(max_length=50, default="50 Pax")
    icon = models.CharField(max_length=100, default="fa-ship text-red-500")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="OPERATIONAL")
    health_score = models.IntegerField(default=100)  # 0-100%
    last_inspected = models.DateField(auto_now=True)
    assigned_decks = models.ManyToManyField('hse_pob.WorkLocation', related_name='assigned_vessels', blank=True)

    def __str__(self):
        return f"{self.name} ({self.vessel.vessel_name})"


# ==========================================
# MACHINERY EQUIPMENT MODEL (Predictive Maintenance)
# ==========================================
class MachineryEquipment(models.Model):
    """Equipment with operating hours tracking for predictive maintenance"""
    id = models.AutoField(primary_key=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE, related_name='machinery_equipment')
    equipment_name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=100)  # ex: Pump, Compressor, Generator
    serial_number = models.CharField(max_length=100, unique=True)
    installation_date = models.DateField()
    operating_hours = models.IntegerField(default=0)  # Total operating hours
    last_maintenance_date = models.DateField(null=True, blank=True)
    maintenance_interval_hours = models.IntegerField(default=1000)  # Hours between maintenance
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment_name} ({self.vessel.vessel_name})"

    @property
    def hours_until_maintenance(self):
        """Calculate hours until next maintenance"""
        return max(0, self.maintenance_interval_hours - self.operating_hours)

    @property
    def needs_maintenance(self):
        """Check if equipment needs maintenance"""
        return self.hours_until_maintenance <= 0


# ==========================================
# SPARE PART MODEL (Inventory Management)
# ==========================================
class SparePart(models.Model):
    """Spare parts inventory"""
    id = models.AutoField(primary_key=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE, related_name='spare_parts')
    part_name = models.CharField(max_length=100)
    part_number = models.CharField(max_length=100, unique=True)
    quantity_on_hand = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=5)  # Alert when stock below this
    supplier = models.CharField(max_length=100, null=True, blank=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.part_name} ({self.vessel.vessel_name})"

    @property
    def low_stock(self):
        """Check if stock is low"""
        return self.quantity_on_hand <= self.reorder_level


# ==========================================
# WORK ORDER MODEL (Moved from hse_ptw)
# ==========================================
class WorkOrder(models.Model):
    """Work Order created by Chief Engineer"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    wo_id = models.CharField(max_length=50, unique=True, primary_key=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE, related_name='work_orders')
    created_by = models.CharField(max_length=100)  # Chief Engineer
    description = models.TextField()
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='MEDIUM')
    scheduled_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.wo_id} - {self.status}"


# ==========================================
# MAINTENANCE TASK MODEL
# ==========================================
class MaintenanceTask(models.Model):
    """Maintenance task linked to equipment and work order"""
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    task_id = models.CharField(max_length=50, primary_key=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE, related_name='maintenance_tasks', null=True, blank=True)
    equipment = models.ForeignKey(MachineryEquipment, on_delete=models.CASCADE, related_name='maintenance_tasks', null=True, blank=True)
    wo_id = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_tasks')
    description = models.TextField()
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="MEDIUM")
    scheduled_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="PENDING")
    # assigned_crew field will be added in a later migration to avoid circular dependency
    completion_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.task_id} - {self.vessel.vessel_name}"


# ==========================================
# INVENTORY ITEM MODEL
# ==========================================
class InventoryItem(models.Model):
    """Inventory items"""
    item_code = models.CharField(max_length=50, primary_key=True)
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="Spare Part")
    current_stock = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=10)
    asset_location = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='inventory', null=True, blank=True)

    def __str__(self):
        return self.item_name
