from django.core.management.base import BaseCommand
from asset_module.models import Vessel, SparePart

class Command(BaseCommand):
    help = 'Seed Spare Parts data for SAIPEM HSE System'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("SAIPEM HSE - Spare Parts Seeder"))
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
                'part_name': 'Engine Oil Filter XL',
                'part_number': 'FLT-OIL-001',
                'quantity_on_hand': 2,
                'reorder_level': 5, # Low stock!
                'supplier': 'MarineParts Global',
                'unit_cost': 45.50
            },
            {
                'vessel': saipem_7000,
                'part_name': 'Generator Spark Plug Set',
                'part_number': 'SPK-GEN-012',
                'quantity_on_hand': 15,
                'reorder_level': 10,
                'supplier': 'Bosch Marine',
                'unit_cost': 120.00
            },
            {
                'vessel': saipem_7000,
                'part_name': 'Main Pump Valve',
                'part_number': 'VLV-PMP-104',
                'quantity_on_hand': 8,
                'reorder_level': 5,
                'supplier': 'Alfa Laval',
                'unit_cost': 350.00
            },
            {
                'vessel': castorone,
                'part_name': 'Thruster V-Belt',
                'part_number': 'BLT-THR-099',
                'quantity_on_hand': 1,
                'reorder_level': 3, # Low stock!
                'supplier': 'Gates Offshore',
                'unit_cost': 85.00
            },
            {
                'vessel': castorone,
                'part_name': 'Hydraulic Seal Kit',
                'part_number': 'SEAL-HYD-500',
                'quantity_on_hand': 20,
                'reorder_level': 15,
                'supplier': 'Parker Hannifin',
                'unit_cost': 25.00
            },
            {
                'vessel': scarabeo_8,
                'part_name': 'Drill Mud Pump Piston',
                'part_number': 'PST-MUD-001',
                'quantity_on_hand': 4,
                'reorder_level': 10, # Low stock!
                'supplier': 'National Oilwell Varco',
                'unit_cost': 850.00
            }
        ]

        for sp_data in spareparts_data:
            part, created = SparePart.objects.update_or_create(
                part_number=sp_data['part_number'],
                defaults={
                    'vessel': sp_data['vessel'],
                    'part_name': sp_data['part_name'],
                    'quantity_on_hand': sp_data['quantity_on_hand'],
                    'reorder_level': sp_data['reorder_level'],
                    'supplier': sp_data['supplier'],
                    'unit_cost': sp_data['unit_cost']
                }
            )
            status = "Low Stock" if part.low_stock else "Optimal"
            if created:
                self.stdout.write(f"✓ Created spare part: {part.part_name} ({part.part_number}) - {status}")
            else:
                self.stdout.write(f"✓ Updated spare part: {part.part_name} ({part.part_number}) - {status}")

        self.stdout.write(f"\n✓ Total spare parts: {SparePart.objects.count()}")
