from django.core.management.base import BaseCommand
from datetime import date
from hse_module.hse_ptw.models import Employee
from asset_module.models import Vessel, Asset, MaintenanceTask, InventoryItem
from hr_module.models import Roster, VesselActivity, Position


class Command(BaseCommand):
    help = 'Seed HR and Asset module data for SAIPEM HSE System'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("SAIPEM HSE - HR & Asset Module Seeder"))
        self.stdout.write("=" * 70)

        # STEP 1: Create Employees
        self.stdout.write("\n[1/8] Creating Employees...")
        employees_data = [
            {
                'emp_id': 'EMP-001',
                'full_name': 'Rick Owens',
                'job_role': 'Chief Engineer',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 12, 31),
                'roster_status': 'ONBOARD'
            },
            {
                'emp_id': 'EMP-002',
                'full_name': 'Martin Margiela',
                'job_role': 'HSE Officer',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 6, 30),
                'roster_status': 'ONBOARD'
            },
            {
                'emp_id': 'EMP-003',
                'full_name': 'Fakemink',
                'job_role': 'Lead Welder',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 9, 15),
                'roster_status': 'ONBOARD'
            },
            {
                'emp_id': 'EMP-004',
                'full_name': 'Lancey Foux',
                'job_role': 'Logistics Manager',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 3, 20),
                'roster_status': 'ONBOARD'
            },
            {
                'emp_id': 'EMP-005',
                'full_name': 'Skepta',
                'job_role': 'Deck Foreman',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 11, 10),
                'roster_status': 'ONBOARD'
            },
            {
                'emp_id': 'EMP-006',
                'full_name': 'Yohji Yamamoto',
                'job_role': 'Rig Manager',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 8, 5),
                'roster_status': 'ONBOARD'
            },
            {
                'emp_id': 'EMP-007',
                'full_name': 'Raf Simons',
                'job_role': 'Scaffolder',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 7, 22),
                'roster_status': 'ONBOARD'
            }
        ]

        for emp_data in employees_data:
            employee, created = Employee.objects.get_or_create(
                emp_id=emp_data['emp_id'],
                defaults={
                    'full_name': emp_data['full_name'],
                    'job_role': emp_data['job_role'],
                    'mcu_status': emp_data['mcu_status'],
                    'mcu_expiry': emp_data['mcu_expiry'],
                    'roster_status': emp_data['roster_status']
                }
            )
            if created:
                self.stdout.write(f"✓ Created employee: {employee.emp_id} - {employee.full_name}")
            else:
                self.stdout.write(f"- Employee already exists: {employee.emp_id}")

        self.stdout.write(f"\n✓ Total employees: {Employee.objects.count()}")

        # STEP 2: Create Vessels (IMPORTANT: Must create before Assets!)
        self.stdout.write("\n[2/8] Creating Vessels...")
        vessels_data = [
            {
                'vessel_name': 'Saipem 7000',
                'vessel_type': 'Drill Ship',
                'imo_number': 'IMO-7000-001',
                'operational_status': 'OPERATIONAL',
                'health_score': 95
            },
            {
                'vessel_name': 'Castorone',
                'vessel_type': 'Crane Vessel',
                'imo_number': 'IMO-CAST-001',
                'operational_status': 'OPERATIONAL',
                'health_score': 90
            },
            {
                'vessel_name': 'Scarabeo 8',
                'vessel_type': 'Jack-up Rig',
                'imo_number': 'IMO-SCAR-001',
                'operational_status': 'OPERATIONAL',
                'health_score': 88
            }
        ]

        vessels = {}
        for vessel_data in vessels_data:
            vessel, created = Vessel.objects.get_or_create(
                vessel_name=vessel_data['vessel_name'],
                defaults={
                    'vessel_type': vessel_data['vessel_type'],
                    'imo_number': vessel_data['imo_number'],
                    'operational_status': vessel_data['operational_status'],
                    'health_score': vessel_data['health_score']
                }
            )
            vessels[vessel_data['vessel_name']] = vessel
            if created:
                self.stdout.write(f"✓ Created vessel: {vessel.vessel_name} ({vessel.vessel_type})")
            else:
                self.stdout.write(f"- Vessel already exists: {vessel.vessel_name}")

        self.stdout.write(f"\n✓ Total vessels: {Vessel.objects.count()}")

        # STEP 3: Create Assets (linked to Vessels)
        self.stdout.write("\n[3/8] Creating Assets (Equipment on Vessels)...")
        assets_data = [
            {
                'asset_id': 'AST-001',
                'vessel_name': 'Saipem 7000',
                'name': 'Main Crane',
                'capacity': '500 Ton',
                'status': 'OPERATIONAL'
            },
            {
                'asset_id': 'AST-002',
                'vessel_name': 'Castorone',
                'name': 'Auxiliary Crane',
                'capacity': '300 Ton',
                'status': 'OPERATIONAL'
            },
            {
                'asset_id': 'AST-003',
                'vessel_name': 'Scarabeo 8',
                'name': 'Drilling Equipment',
                'capacity': '150 Ton',
                'status': 'OPERATIONAL'
            }
        ]

        assets = {}
        for asset_data in assets_data:
            try:
                vessel = vessels[asset_data['vessel_name']]
                asset, created = Asset.objects.get_or_create(
                    asset_id=asset_data['asset_id'],
                    defaults={
                        'vessel': vessel,
                        'name': asset_data['name'],
                        'capacity': asset_data['capacity'],
                        'status': asset_data['status']
                    }
                )
                assets[asset_data['asset_id']] = asset
                if created:
                    self.stdout.write(f"✓ Created asset: {asset.asset_id} - {asset.name} on {vessel.vessel_name}")
                else:
                    self.stdout.write(f"- Asset already exists: {asset.asset_id}")
            except KeyError:
                self.stdout.write(self.style.WARNING(f"⚠ Vessel {asset_data['vessel_name']} not found for asset {asset_data['asset_id']}"))

        self.stdout.write(f"\n✓ Total assets: {Asset.objects.count()}")

        # STEP 4: Create Positions
        self.stdout.write("\n[4/8] Creating Position Master Data...")
        positions_data = [
            {
                'title': 'Chief Engineer',
                'discipline': 'Marine',
                'daily_rate': 500000,
                'allowance_rate': 300000
            },
            {
                'title': 'HSE Officer',
                'discipline': 'Safety',
                'daily_rate': 400000,
                'allowance_rate': 250000
            },
            {
                'title': 'Lead Welder',
                'discipline': 'Marine',
                'daily_rate': 350000,
                'allowance_rate': 200000
            },
            {
                'title': 'Logistics Manager',
                'discipline': 'Marine',
                'daily_rate': 380000,
                'allowance_rate': 220000
            },
            {
                'title': 'Deck Foreman',
                'discipline': 'Marine',
                'daily_rate': 320000,
                'allowance_rate': 180000
            },
            {
                'title': 'Rig Manager',
                'discipline': 'Drilling',
                'daily_rate': 550000,
                'allowance_rate': 350000
            },
            {
                'title': 'Scaffolder',
                'discipline': 'Marine',
                'daily_rate': 300000,
                'allowance_rate': 150000
            }
        ]

        for pos_data in positions_data:
            position, created = Position.objects.get_or_create(
                title=pos_data['title'],
                defaults={
                    'discipline': pos_data['discipline'],
                    'daily_rate': pos_data['daily_rate'],
                    'allowance_rate': pos_data['allowance_rate']
                }
            )
            if created:
                self.stdout.write(f"✓ Created position: {position.title} ({position.discipline})")
            else:
                self.stdout.write(f"- Position already exists: {position.title}")

        self.stdout.write(f"\n✓ Total positions: {Position.objects.count()}")

        # STEP 5: Create Rosters (linked to Vessels, not Assets)
        self.stdout.write("\n[5/8] Creating Roster Schedules...")
        rosters_data = [
            {
                'emp_id': 'EMP-001',
                'vessel_name': 'Saipem 7000',
                'start_date': date(2026, 5, 1),
                'end_date': date(2026, 6, 15)
            },
            {
                'emp_id': 'EMP-003',
                'vessel_name': 'Saipem 7000',
                'start_date': date(2026, 5, 10),
                'end_date': date(2026, 6, 20)
            },
            {
                'emp_id': 'EMP-005',
                'vessel_name': 'Castorone',
                'start_date': date(2026, 5, 20),
                'end_date': date(2026, 7, 1)
            },
            {
                'emp_id': 'EMP-002',
                'vessel_name': 'Saipem 7000',
                'start_date': date(2026, 6, 1),
                'end_date': date(2026, 6, 30)
            }
        ]

        for i, roster_data in enumerate(rosters_data, 1):
            try:
                employee = Employee.objects.get(emp_id=roster_data['emp_id'])
                vessel = vessels[roster_data['vessel_name']]

                roster, created = Roster.objects.get_or_create(
                    employee=employee,
                    vessel=vessel,
                    start_date=roster_data['start_date'],
                    defaults={'end_date': roster_data['end_date']}
                )
                if created:
                    self.stdout.write(f"✓ Created roster: {employee.full_name} -> {vessel.vessel_name}")
                else:
                    self.stdout.write(f"- Roster already exists: {employee.emp_id}")
            except (Employee.DoesNotExist, KeyError) as e:
                self.stdout.write(self.style.WARNING(f"⚠ Skipped roster {i}: {str(e)}"))

        self.stdout.write(f"\n✓ Total rosters: {Roster.objects.count()}")

        # STEP 6: Create Vessel Activities
        self.stdout.write("\n[6/8] Creating Vessel Activities...")
        activities_data = [
            {
                'vessel_name': 'Saipem 7000',
                'start_date': date(2026, 5, 1),
                'end_date': date(2026, 5, 15),
                'activity_name': 'Offshore Drilling Operations'
            },
            {
                'vessel_name': 'Castorone',
                'start_date': date(2026, 5, 20),
                'end_date': date(2026, 6, 10),
                'activity_name': 'Rig Maintenance & Inspection'
            },
            {
                'vessel_name': 'Scarabeo 8',
                'start_date': date(2026, 6, 1),
                'end_date': date(2026, 6, 5),
                'activity_name': 'Emergency Repair Operations'
            }
        ]

        for activity_data in activities_data:
            try:
                vessel = vessels[activity_data['vessel_name']]
                activity, created = VesselActivity.objects.get_or_create(
                    vessel=vessel,
                    start_date=activity_data['start_date'],
                    defaults={
                        'end_date': activity_data['end_date'],
                        'activity_name': activity_data['activity_name']
                    }
                )
                if created:
                    self.stdout.write(f"✓ Created activity: {activity.activity_name}")
                else:
                    self.stdout.write(f"- Activity already exists")
            except KeyError:
                self.stdout.write(self.style.WARNING(f"⚠ Vessel not found for activity"))

        self.stdout.write(f"\n✓ Total activities: {VesselActivity.objects.count()}")

        # STEP 7: Create Inventory Items (linked to Assets)
        self.stdout.write("\n[7/8] Creating Inventory Items...")
        inventory_data = [
            {
                'item_code': 'INV-001',
                'item_name': 'Drill Pipe 5-inch',
                'category': 'Spare Parts',
                'current_stock': 120,
                'minimum_stock': 50,
                'asset_id': 'AST-001'
            },
            {
                'item_code': 'INV-002',
                'item_name': 'Safety Harness',
                'category': 'Safety Equipment',
                'current_stock': 45,
                'minimum_stock': 20,
                'asset_id': 'AST-002'
            },
            {
                'item_code': 'INV-003',
                'item_name': 'Marine Lubricant Oil',
                'category': 'Consumables',
                'current_stock': 5,
                'minimum_stock': 20,
                'asset_id': 'AST-002'
            },
            {
                'item_code': 'INV-004',
                'item_name': 'Welding Electrodes',
                'category': 'Consumables',
                'current_stock': 2,
                'minimum_stock': 50,
                'asset_id': 'AST-003'
            },
            {
                'item_code': 'INV-005',
                'item_name': 'Hydraulic Fluid ISO 46',
                'category': 'Consumables',
                'current_stock': 200,
                'minimum_stock': 100,
                'asset_id': 'AST-001'
            }
        ]

        for item_data in inventory_data:
            try:
                asset_location = assets[item_data['asset_id']]
                item, created = InventoryItem.objects.get_or_create(
                    item_code=item_data['item_code'],
                    defaults={
                        'item_name': item_data['item_name'],
                        'category': item_data['category'],
                        'current_stock': item_data['current_stock'],
                        'minimum_stock': item_data['minimum_stock'],
                        'asset_location': asset_location
                    }
                )
                if created:
                    status = "AMAN" if item.current_stock > item.minimum_stock else "KRITIS"
                    self.stdout.write(f"✓ Created inventory: {item.item_code} ({item.current_stock} units) - {status}")
                else:
                    self.stdout.write(f"- Inventory already exists: {item.item_code}")
            except KeyError:
                self.stdout.write(self.style.WARNING(f"⚠ Asset {item_data['asset_id']} not found for inventory {item_data['item_code']}"))

        self.stdout.write(f"\n✓ Total inventory items: {InventoryItem.objects.count()}")

        # STEP 8: Create Maintenance Tasks (linked to Vessels)
        self.stdout.write("\n[8/8] Creating Maintenance Tasks...")
        maintenance_data = [
            {
                'task_id': 'MT-001',
                'vessel_name': 'Scarabeo 8',
                'description': 'Generator Engine Overhaul - Complete rebuild and testing',
                'scheduled_date': date(2026, 6, 1),
                'status': 'PENDING',
                'priority': 'CRITICAL',
                'assigned_crew_id': 'EMP-001'
            },
            {
                'task_id': 'MT-002',
                'vessel_name': 'Castorone',
                'description': 'Crane Cable Inspection and Certification',
                'scheduled_date': date(2026, 6, 5),
                'status': 'PENDING',
                'priority': 'HIGH',
                'assigned_crew_id': 'EMP-005'
            },
            {
                'task_id': 'MT-003',
                'vessel_name': 'Saipem 7000',
                'description': 'HVAC Filter Replacement and System Check',
                'scheduled_date': date(2026, 6, 10),
                'status': 'PENDING',
                'priority': 'MEDIUM',
                'assigned_crew_id': 'EMP-007'
            },
            {
                'task_id': 'MT-004',
                'vessel_name': 'Saipem 7000',
                'description': 'Annual Fire Suppression System Inspection',
                'scheduled_date': date(2026, 6, 15),
                'status': 'PENDING',
                'priority': 'CRITICAL',
                'assigned_crew_id': 'EMP-002'
            }
        ]

        for task_data in maintenance_data:
            try:
                vessel = vessels[task_data['vessel_name']]
                assigned_crew = Employee.objects.get(emp_id=task_data['assigned_crew_id'])

                task, created = MaintenanceTask.objects.get_or_create(
                    task_id=task_data['task_id'],
                    defaults={
                        'vessel': vessel,
                        'description': task_data['description'],
                        'scheduled_date': task_data['scheduled_date'],
                        'status': task_data['status'],
                        'priority': task_data['priority'],
                        'assigned_crew': assigned_crew
                    }
                )
                if created:
                    self.stdout.write(f"✓ Created maintenance: {task.task_id} ({task.priority}) - {vessel.vessel_name}")
                else:
                    self.stdout.write(f"- Maintenance already exists: {task.task_id}")
            except (KeyError, Employee.DoesNotExist) as e:
                self.stdout.write(self.style.WARNING(f"⚠ Error creating task {task_data['task_id']}: {str(e)}"))

        self.stdout.write(f"\n✓ Total maintenance tasks: {MaintenanceTask.objects.count()}")

        # SUMMARY
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("✅ SEEDING COMPLETE!"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"✓ Employees: {Employee.objects.count()}")
        self.stdout.write(f"✓ Vessels: {Vessel.objects.count()}")
        self.stdout.write(f"✓ Assets: {Asset.objects.count()}")
        self.stdout.write(f"✓ Positions: {Position.objects.count()}")
        self.stdout.write(f"✓ Rosters: {Roster.objects.count()}")
        self.stdout.write(f"✓ Vessel Activities: {VesselActivity.objects.count()}")
        self.stdout.write(f"✓ Inventory Items: {InventoryItem.objects.count()}")
        self.stdout.write(f"✓ Maintenance Tasks: {MaintenanceTask.objects.count()}")
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("🚀 Ready for testing!"))
