# Generated migration to add missing fields

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hse_pob', '0001_initial'),
        ('hse_ptw', '0001_initial'),
        ('asset_module', '0001_initial'),
    ]

    operations = [
        # Add assigned_decks M2M field to Vessel
        migrations.AddField(
            model_name='vessel',
            name='assigned_decks',
            field=models.ManyToManyField(blank=True, related_name='vessels', to='hse_pob.worklocation'),
        ),
        # Add asset_location FK to InventoryItem
        migrations.AddField(
            model_name='inventoryitem',
            name='asset_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='asset_module.asset'),
        ),
        # Add assigned_crew FK to MaintenanceTask
        migrations.AddField(
            model_name='maintenancetask',
            name='assigned_crew',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hse_ptw.employee'),
        ),
        # Add equipment FK to MaintenanceTask
        migrations.AddField(
            model_name='maintenancetask',
            name='equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_tasks', to='asset_module.machineryequipment'),
        ),
        # Add wo_id FK to MaintenanceTask
        migrations.AddField(
            model_name='maintenancetask',
            name='wo_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintenance_tasks', to='asset_module.workorder'),
        ),
    ]
