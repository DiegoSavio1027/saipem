from django.core.management.base import BaseCommand
from asset_module.models import Vessel, InventoryItem

class Command(BaseCommand):
    help = 'Seed Spare Parts data for SAIPEM HSE System'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("SAIPEM HSE - Inventory Seeder"))
        self.stdout.write("=" * 70)

        # Get existing vessels
        try:
            saipem_7000 = Vessel.objects.get(vessel_name='Saipem 7000')
            castorone = Vessel.objects.get(vessel_name='Castorone')
            scarabeo_8 = Vessel.objects.get(vessel_name='Scarabeo 8')
        except Vessel.DoesNotExist:
            self.stdout.write(self.style.ERROR("Vessels not found. Run seed_hr_asset_data first."))
            return

        spareparts_data = [
            {
                'vessel': saipem_7000,
                'item_name': 'Engine Oil Filter XL',
                'item_code': 'FLT-OIL-001',
                'category': 'Spare Part',
                'current_stock': 2,
                'minimum_stock': 5, # Low stock!
                'supplier': 'MarineParts Global',
                'unit_cost': 45.50
            },
            {
                'vessel': saipem_7000,
                'item_name': 'Generator Spark Plug Set',
                'item_code': 'SPK-GEN-012',
                'category': 'Spare Part',
                'current_stock': 15,
                'minimum_stock': 10,
                'supplier': 'Bosch Marine',
                'unit_cost': 120.00
            },
            {
                'vessel': saipem_7000,
                'item_name': 'Main Pump Valve',
                'item_code': 'VLV-PMP-104',
                'category': 'Spare Part',
                'current_stock': 8,
                'minimum_stock': 5,
                'supplier': 'Alfa Laval',
                'unit_cost': 350.00
            },
            {
                'vessel': castorone,
                'item_name': 'Thruster V-Belt',
                'item_code': 'BLT-THR-099',
                'category': 'Spare Part',
                'current_stock': 1,
                'minimum_stock': 3, # Low stock!
                'supplier': 'Gates Offshore',
                'unit_cost': 85.00
            },
            {
                'vessel': castorone,
                'item_name': 'Hydraulic Seal Kit',
                'item_code': 'SEAL-HYD-500',
                'category': 'Spare Part',
                'current_stock': 20,
                'minimum_stock': 15,
                'supplier': 'Parker Hannifin',
                'unit_cost': 25.00
            },
            {
                'vessel': scarabeo_8,
                'item_name': 'Drill Mud Pump Piston',
                'item_code': 'PST-MUD-001',
                'category': 'Spare Part',
                'current_stock': 4,
                'minimum_stock': 10, # Low stock!
                'supplier': 'National Oilwell Varco',
                'unit_cost': 850.00
            }
        ]

        for sp_data in spareparts_data:
            part, created = InventoryItem.objects.update_or_create(
                item_code=sp_data['item_code'],
                defaults={
                    'vessel': sp_data['vessel'],
                    'item_name': sp_data['item_name'],
                    'category': sp_data['category'],
                    'current_stock': sp_data['current_stock'],
                    'minimum_stock': sp_data['minimum_stock'],
                    'supplier': sp_data['supplier'],
                    'unit_cost': sp_data['unit_cost']
                }
            )
            status = "Low Stock" if part.current_stock <= part.minimum_stock else "Optimal"
            if created:
                self.stdout.write(f"✓ Created inventory item: {part.item_name} ({part.item_code}) - {status}")
            else:
                self.stdout.write(f"✓ Updated inventory item: {part.item_name} ({part.item_code}) - {status}")

        self.stdout.write(f"\n✓ Total inventory items: {InventoryItem.objects.count()}")
