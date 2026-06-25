import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core_system.settings")
django.setup()

from asset_module.models import WorkOrder, Vessel
from hr_module.models import Employee

vessel = Vessel.objects.first()
emp = Employee.objects.first()

wo = WorkOrder.objects.create(
    vessel=vessel,
    description='Test Auto WO ID',
    scheduled_date='2026-06-25',
    created_by='Test',
    assigned_to=emp
)

print(f"Created WO with ID: {wo.wo_id}")
