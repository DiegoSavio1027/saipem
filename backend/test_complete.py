import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core_system.settings")
django.setup()

from asset_module.models import WorkOrder, InventoryItem, WorkOrderMaterial
from django.utils import timezone

item = InventoryItem.objects.first()
print(f"Before: {item.item_code} - Current: {item.current_stock} - Reserved: {item.quantity_reserved}")

wo = WorkOrder.objects.create(
    wo_id="TEST-WO-1",
    description="Test",
    status="WAITING_REVIEW",
    scheduled_date=timezone.now().date()
)

mat = WorkOrderMaterial.objects.create(
    work_order=wo,
    inventory_item=item,
    quantity_used=5
)
item.quantity_reserved += 5
item.save()
print(f"After Add: {item.item_code} - Current: {item.current_stock} - Reserved: {item.quantity_reserved}")

old_status = wo.status
new_status = 'COMPLETED'
if old_status != 'COMPLETED' and new_status == 'COMPLETED':
    for material in wo.materials.all():
        inv_item = material.inventory_item
        print(f"Deducting {material.quantity_used} from {inv_item.item_code}")
        inv_item.current_stock -= material.quantity_used
        inv_item.quantity_reserved -= material.quantity_used
        inv_item.save()

item.refresh_from_db()
print(f"After Complete: {item.item_code} - Current: {item.current_stock} - Reserved: {item.quantity_reserved}")
wo.delete()
item.current_stock = 120
item.quantity_reserved = 0
item.save()
