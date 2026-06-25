from django.core.management.base import BaseCommand
from datetime import date, timedelta
from hr_module.models import Employee
from asset_module.models import Vessel, Asset, MaintenanceTask, InventoryItem, MachineryEquipment, WorkOrder
from hr_module.models import Roster, VesselActivity, Position
from hse_module.hse_pob.models import WorkLocation
from django.contrib.auth.models import User, Group



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
                'emp_id': 'chief_engineer_hq',
                'full_name': 'Johan HQ',
                'job_role': 'Chief Engineer',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 12, 31),
                'roster_status': 'AVAILABLE',
                'email': 'chief_hq@saipem.com'
            },
            {
                'emp_id': 'chief_engineer_castorone',
                'full_name': 'Johan Castorone',
                'job_role': 'Chief Engineer',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 12, 31),
                'roster_status': 'ONBOARD',
                'email': 'chief_castorone@saipem.com'
            },
            {
                'emp_id': 'safety_officer_hq',
                'full_name': 'Diego HQ',
                'job_role': 'Safety Officer',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 6, 30),
                'roster_status': 'AVAILABLE',
                'email': 'safety_hq@saipem.com'
            },
            {
                'emp_id': 'safety_officer_castorone',
                'full_name': 'Diego Castorone',
                'job_role': 'Safety Officer',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 6, 30),
                'roster_status': 'ONBOARD',
                'email': 'safety_castorone@saipem.com'
            },

            {
                'emp_id': 'chief_engineer_s7000',
                'full_name': 'Johan Branson',
                'job_role': 'Chief Engineer',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 12, 31),
                'roster_status': 'ONBOARD',
                'email': 'chief@saipem.com'
            },
            {
                'emp_id': 'safety_officer_s7000',
                'full_name': 'Diego Savio',
                'job_role': 'Safety Officer',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 6, 30),
                'roster_status': 'ONBOARD',
                'email': 'safety@saipem.com'
            },
            {
                'emp_id': 'worker',
                'full_name': 'Aron Piper',
                'job_role': 'Worker',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 9, 15),
                'roster_status': 'ONBOARD',
                'email': 'worker@saipem.com'
            },
            {
                'emp_id': 'hr_staff',
                'full_name': 'Ijlal Nuhlan',
                'job_role': 'HR Staff',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 3, 20),
                'roster_status': 'AVAILABLE',
                'email': 'hr@saipem.com'
            },
            {
                'emp_id': 'EMP-005',
                'full_name': 'Skepta',
                'job_role': 'Deck Foreman',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 11, 10),
                'roster_status': 'ONBOARD',
                'email': 'skepta@saipem.com'
            },
            {
                'emp_id': 'EMP-006',
                'full_name': 'Yohji Yamamoto',
                'job_role': 'Rig Manager',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 8, 5),
                'roster_status': 'AVAILABLE',
                'email': 'yohji@saipem.com'
            },
            {
                'emp_id': 'EMP-007',
                'full_name': 'Raf Simons',
                'job_role': 'Scaffolder',
                'mcu_status': 'FIT',
                'mcu_expiry': date(2027, 7, 22),
                'roster_status': 'AVAILABLE',
                'email': 'raf@saipem.com'
            }
        ]

        # Ensure Groups exist
        groups_data = ['Admin', 'HR Staff', 'Chief Engineer', 'Worker', 'Safety Officer']
        for group_name in groups_data:
            Group.objects.get_or_create(name=group_name)

        # Mapping for roles and default passwords
        group_mapping = {
            'System Administrator': 'Admin',
            'HR Staff': 'HR Staff',
            'Chief Engineer': 'Chief Engineer',
            'Safety Officer': 'Safety Officer',
            'Worker': 'Worker',
            'Deck Foreman': 'Worker',
            'Rig Manager': 'Worker',
            'Scaffolder': 'Worker',
        }

        password_mapping = {
            'chief_engineer_hq': 'chief123',
            'chief_engineer_castorone': 'chief123',
            'safety_officer_hq': 'safety123',
            'safety_officer_castorone': 'safety123',

            'admin': 'admin123',
            'hr_staff': 'hr123',
            'chief_engineer_s7000': 'chief123',
            'worker': 'worker123',
            'safety_officer_s7000': 'safety123',
        }

        for emp_data in employees_data:
            # 1. Update/Create Employee record
            employee, created = Employee.objects.update_or_create(
                emp_id=emp_data['emp_id'],
                defaults={
                    'full_name': emp_data['full_name'],
                    'job_role': emp_data['job_role'],
                    'mcu_status': emp_data['mcu_status'],
                    'mcu_expiry': emp_data['mcu_expiry'],
                    'roster_status': emp_data['roster_status'],
                    'email': emp_data['email']
                }
            )
            if created:
                self.stdout.write(f"✓ Created employee: {employee.emp_id} - {employee.full_name}")
            else:
                self.stdout.write(f"✓ Updated employee: {employee.emp_id} - {employee.full_name}")

            # 2. Update/Create Django User account for authentication
            names = emp_data['full_name'].split(' ', 1)
            first_name = names[0]
            last_name = names[1] if len(names) > 1 else ''
            username = emp_data['emp_id']
            email = emp_data['email']
            group_name = group_mapping.get(emp_data['job_role'], 'Worker')
            password = password_mapping.get(username, 'saipem123')

            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_superuser': (group_name == 'Admin'),
                    'is_staff': (group_name == 'Admin')
                }
            )
            # Enforce password and group membership
            user.set_password(password)
            user.save()
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            
            if user_created:
                self.stdout.write(f"  ✓ Created login account for '{username}' (Password: '{password}', Role: '{group_name}')")
            else:
                self.stdout.write(f"  ✓ Ensured login account exists for '{username}' (Password: '{password}', Role: '{group_name}')")

            # 3. Synchronize UserProfile
            if hasattr(user, 'profile'):
                user.profile.job_role = emp_data['job_role']
                user.profile.roster_status = emp_data['roster_status']
                user.profile.mcu_status = emp_data['mcu_status']
                user.profile.mcu_expiry = emp_data['mcu_expiry']
                user.profile.save()

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
        all_decks = list(WorkLocation.objects.all())
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
            
            # Link all standard decks to this vessel
            if all_decks:
                vessel.assigned_decks.add(*all_decks)
                
            if created:
                self.stdout.write(f"✓ Created vessel: {vessel.vessel_name} ({vessel.vessel_type}) and linked {len(all_decks)} decks")
            else:
                self.stdout.write(f"- Vessel already exists: {vessel.vessel_name}")

        self.stdout.write(f"\n✓ Total vessels: {Vessel.objects.count()}")

        # STEP 3: Create Assets (linked to Vessels)
        self.stdout.write("\n[3/8] Creating Assets (Equipment on Vessels)...")
        assets_data = [
            # Saipem 7000
            {
                'asset_id': 'AST-001',
                'vessel_name': 'Saipem 7000',
                'name': 'Main Crane',
                'capacity': '500 Ton',
                'status': 'OPERATIONAL',
                'health_score': 95,
                'deck_name': 'Main Deck'
            },
            {
                'asset_id': 'AST-004',
                'vessel_name': 'Saipem 7000',
                'name': 'Helideck Safety System',
                'capacity': 'Standard',
                'status': 'CRITICAL',
                'health_score': 30,
                'deck_name': 'Heli Deck'
            },
            {
                'asset_id': 'AST-005',
                'vessel_name': 'Saipem 7000',
                'name': 'Pipe Laying Tensioner',
                'capacity': '250 Ton',
                'status': 'MAINTENANCE',
                'health_score': 75,
                'deck_name': 'Main Deck'
            },
            {
                'asset_id': 'AST-006',
                'vessel_name': 'Saipem 7000',
                'name': 'Lifeboat Station A',
                'capacity': '50 Pax',
                'status': 'OPERATIONAL',
                'health_score': 100,
                'deck_name': 'Upper Deck'
            },
            # Castorone
            {
                'asset_id': 'AST-002',
                'vessel_name': 'Castorone',
                'name': 'Auxiliary Crane',
                'capacity': '300 Ton',
                'status': 'OPERATIONAL',
                'health_score': 92,
                'deck_name': 'Main Deck'
            },
            {
                'asset_id': 'AST-007',
                'vessel_name': 'Castorone',
                'name': 'Stinger Control System',
                'capacity': 'Standard',
                'status': 'CRITICAL',
                'health_score': 20,
                'deck_name': 'Main Deck'
            },
            {
                'asset_id': 'AST-008',
                'vessel_name': 'Castorone',
                'name': 'Ballast Control Console',
                'capacity': 'Standard',
                'status': 'OPERATIONAL',
                'health_score': 98,
                'deck_name': 'Engine Room'
            },
            # Scarabeo 8
            {
                'asset_id': 'AST-003',
                'vessel_name': 'Scarabeo 8',
                'name': 'Drilling Equipment',
                'capacity': '150 Ton',
                'status': 'OPERATIONAL',
                'health_score': 90,
                'deck_name': 'Machinery Space'
            },
            {
                'asset_id': 'AST-009',
                'vessel_name': 'Scarabeo 8',
                'name': 'Blowout Preventer (BOP)',
                'capacity': '10k PSI',
                'status': 'CRITICAL',
                'health_score': 15,
                'deck_name': 'Lower Deck'
            },
            {
                'asset_id': 'AST-010',
                'vessel_name': 'Scarabeo 8',
                'name': 'Top Drive System',
                'capacity': '800 HP',
                'status': 'MAINTENANCE',
                'health_score': 60,
                'deck_name': 'Main Deck'
            }
        ]

        assets = {}
        for asset_data in assets_data:
            try:
                vessel = vessels[asset_data['vessel_name']]
                asset, created = Asset.objects.update_or_create(
                    asset_id=asset_data['asset_id'],
                    defaults={
                        'vessel': vessel,
                        'name': asset_data['name'],
                        'capacity': asset_data['capacity'],
                        'status': asset_data['status'],
                        'health_score': asset_data['health_score']
                    }
                )
                assets[asset_data['asset_id']] = asset
                
                # Link deck location to this asset
                if asset_data['deck_name']:
                    deck = WorkLocation.objects.filter(deck_name=asset_data['deck_name']).first()
                    if deck:
                        asset.assigned_decks.add(deck)
                        
                if created:
                    self.stdout.write(f"✓ Created asset: {asset.asset_id} - {asset.name} on {vessel.vessel_name} (Location: {asset_data['deck_name']})")
                else:
                    self.stdout.write(f"✓ Updated asset: {asset.asset_id} - {asset.name} on {vessel.vessel_name} (Location: {asset_data['deck_name']})")
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
        # Clear existing rosters to prevent duplicate get_or_create errors
        Roster.objects.all().delete()
        
        today_date = date.today()
        rosters_data = [
            {
                'emp_id': 'chief_engineer_castorone',
                'vessel_name': 'Castorone',
                'start_date': today_date - timedelta(days=15),
                'end_date': today_date + timedelta(days=30)
            },
            {
                'emp_id': 'safety_officer_castorone',
                'vessel_name': 'Castorone',
                'start_date': today_date - timedelta(days=15),
                'end_date': today_date + timedelta(days=30)
            },

            {
                'emp_id': 'chief_engineer_s7000',
                'vessel_name': 'Saipem 7000',
                'start_date': today_date - timedelta(days=15),
                'end_date': today_date + timedelta(days=30)
            },
            {
                'emp_id': 'worker',
                'vessel_name': 'Saipem 7000',
                'start_date': today_date - timedelta(days=15),
                'end_date': today_date + timedelta(days=30)
            },
            {
                'emp_id': 'EMP-005',
                'vessel_name': 'Castorone',
                'start_date': today_date - timedelta(days=15),
                'end_date': today_date + timedelta(days=30)
            },
            {
                'emp_id': 'safety_officer_s7000',
                'vessel_name': 'Saipem 7000',
                'start_date': today_date - timedelta(days=15),
                'end_date': today_date + timedelta(days=30)
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
        # Clear existing activities to prevent duplicate get_or_create errors
        VesselActivity.objects.all().delete()
        
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
                'assigned_crew_id': 'chief_engineer_s7000'
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
                'assigned_crew_id': 'safety_officer_s7000'
            }
        ]

        for task_data in maintenance_data:
            try:
                vessel = vessels[task_data['vessel_name']]
                # assigned_crew field temporarily removed to break circular dependency
                # assigned_crew = Employee.objects.get(emp_id=task_data['assigned_crew_id'])

                task, created = MaintenanceTask.objects.get_or_create(
                    task_id=task_data['task_id'],
                    defaults={
                        'vessel': vessel,
                        'description': task_data['description'],
                        'scheduled_date': task_data['scheduled_date'],
                        'status': task_data['status'],
                        'priority': task_data['priority'],
                        # 'assigned_crew': assigned_crew  # Will be added back in a later migration
                    }
                )
                if created:
                    self.stdout.write(f"✓ Created maintenance: {task.task_id} ({task.priority}) - {vessel.vessel_name}")
                else:
                    self.stdout.write(f"- Maintenance already exists: {task.task_id}")
            except (KeyError, Employee.DoesNotExist) as e:
                self.stdout.write(self.style.WARNING(f"⚠ Error creating task {task_data['task_id']}: {str(e)}"))

        self.stdout.write(f"\n✓ Total maintenance tasks: {MaintenanceTask.objects.count()}")

        # STEP 9: Create Machinery Equipment
        self.stdout.write("\n[9/9] Creating Machinery Equipment (IoT Telemetry)...")
        machinery_data = [
            {
                'vessel_name': 'Saipem 7000',
                'equipment_name': 'Main Generator A',
                'equipment_type': 'Generator',
                'serial_number': 'GEN-S7000-001',
                'installation_date': date(2022, 1, 15),
                'operating_hours': 850,
                'maintenance_interval_hours': 1000,
                'last_maintenance_date': date(2025, 12, 1),
                'asset_id': 'AST-001'
            },
            {
                'vessel_name': 'Saipem 7000',
                'equipment_name': 'Main Generator B',
                'equipment_type': 'Generator',
                'serial_number': 'GEN-S7000-002',
                'installation_date': date(2022, 1, 15),
                'operating_hours': 1050,  # OVERDUE! needs_maintenance = True
                'maintenance_interval_hours': 1000,
                'last_maintenance_date': date(2025, 11, 15),
                'asset_id': 'AST-005'
            },
            {
                'vessel_name': 'Saipem 7000',
                'equipment_name': 'Main Ballast Pump 1',
                'equipment_type': 'Pump',
                'serial_number': 'PMP-S7000-001',
                'installation_date': date(2023, 4, 10),
                'operating_hours': 450,
                'maintenance_interval_hours': 1200,
                'last_maintenance_date': date(2026, 1, 10),
                'asset_id': 'AST-005'
            },
            {
                'vessel_name': 'Saipem 7000',
                'equipment_name': 'Air Compressor A',
                'equipment_type': 'Compressor',
                'serial_number': 'CMP-S7000-001',
                'installation_date': date(2023, 6, 20),
                'operating_hours': 1220,  # OVERDUE! needs_maintenance = True
                'maintenance_interval_hours': 1200,
                'last_maintenance_date': date(2025, 12, 20),
                'asset_id': 'AST-006'
            },
            {
                'vessel_name': 'Castorone',
                'equipment_name': 'Propulsion Thruster 1',
                'equipment_type': 'Thruster',
                'serial_number': 'THR-CAST-001',
                'installation_date': date(2021, 9, 5),
                'operating_hours': 920,
                'maintenance_interval_hours': 1000,
                'last_maintenance_date': date(2025, 10, 1),
                'asset_id': 'AST-008'
            },
            {
                'vessel_name': 'Castorone',
                'equipment_name': 'Hydraulic Power Unit A',
                'equipment_type': 'Hydraulic Unit',
                'serial_number': 'HPU-CAST-001',
                'installation_date': date(2022, 3, 12),
                'operating_hours': 1580,  # OVERDUE! needs_maintenance = True
                'maintenance_interval_hours': 1500,
                'last_maintenance_date': date(2025, 9, 12),
                'asset_id': 'AST-007'
            },
            {
                'vessel_name': 'Scarabeo 8',
                'equipment_name': 'Drill Mud Pump A',
                'equipment_type': 'Pump',
                'serial_number': 'PMP-SCAR-001',
                'installation_date': date(2024, 2, 1),
                'operating_hours': 200,
                'maintenance_interval_hours': 1000,
                'last_maintenance_date': date(2026, 2, 1),
                'asset_id': 'AST-003'
            },
            {
                'vessel_name': 'Scarabeo 8',
                'equipment_name': 'Emergency Generator',
                'equipment_type': 'Generator',
                'serial_number': 'GEN-SCAR-003',
                'installation_date': date(2023, 8, 14),
                'operating_hours': 490,
                'maintenance_interval_hours': 500,
                'last_maintenance_date': date(2026, 1, 14),
                'asset_id': 'AST-009'
            }
        ]

        for mac_data in machinery_data:
            try:
                vessel = vessels[mac_data['vessel_name']]
                asset = assets.get(mac_data.get('asset_id'))
                mac, created = MachineryEquipment.objects.update_or_create(
                    serial_number=mac_data['serial_number'],
                    defaults={
                        'vessel': vessel,
                        'asset': asset,
                        'equipment_name': mac_data['equipment_name'],
                        'equipment_type': mac_data['equipment_type'],
                        'installation_date': mac_data['installation_date'],
                        'operating_hours': mac_data['operating_hours'],
                        'maintenance_interval_hours': mac_data['maintenance_interval_hours'],
                        'last_maintenance_date': mac_data['last_maintenance_date']
                    }
                )
                if created:
                    self.stdout.write(f"✓ Created machinery: {mac.equipment_name} ({mac.serial_number}) on {vessel.vessel_name}")
                else:
                    self.stdout.write(f"✓ Updated machinery: {mac.equipment_name} ({mac.serial_number}) on {vessel.vessel_name}")
            except KeyError:
                self.stdout.write(self.style.WARNING(f"⚠ Vessel {mac_data['vessel_name']} not found for machinery {mac_data['serial_number']}"))

        self.stdout.write(f"\n✓ Total machinery equipment: {MachineryEquipment.objects.count()}")

        # STEP 10: Create Work Orders (linked to Vessel, Asset, and Machinery)
        self.stdout.write("\n[10/10] Creating Work Orders...")
        # Clear existing work orders to prevent duplicate key/conflict errors
        WorkOrder.objects.all().delete()

        work_orders_data = [
            # Saipem 7000
            {
                'wo_id': 'WO-2024-001',
                'vessel_name': 'Saipem 7000',
                'machinery_serial': 'GEN-S7000-001', # Main Generator A
                'asset_id': None,
                'description': 'Engine Room Maintenance - Routine inspection and lubrication of Main Generator A',
                'priority': 'MEDIUM',
                'status': 'PENDING',
                'scheduled_date': date.today() + timedelta(days=1),
                'created_by': 'chief_engineer_s7000'
            },
            {
                'wo_id': 'WO-2024-002',
                'vessel_name': 'Saipem 7000',
                'machinery_serial': None,
                'asset_id': 'AST-005', # Pipe Laying Tensioner
                'description': 'Pipe Laying Tensioner Maintenance - Painting and rust prevention',
                'priority': 'MEDIUM',
                'status': 'PENDING',
                'scheduled_date': date.today() + timedelta(days=2),
                'created_by': 'chief_engineer_s7000'
            },
            {
                'wo_id': 'WO-2024-003',
                'vessel_name': 'Saipem 7000',
                'machinery_serial': 'PMP-S7000-001', # Main Ballast Pump 1
                'asset_id': None,
                'description': 'Confined Space Entry - Ballast tank inspection and Main Ballast Pump 1 check',
                'priority': 'HIGH',
                'status': 'PENDING',
                'scheduled_date': date.today() + timedelta(days=3),
                'created_by': 'chief_engineer_s7000'
            },
            {
                'wo_id': 'WO-2024-004',
                'vessel_name': 'Saipem 7000',
                'machinery_serial': None,
                'asset_id': 'AST-005', # Pipe Laying Tensioner
                'description': 'Hot Work - Welding repair on Pipe Laying Tensioner structure',
                'priority': 'HIGH',
                'status': 'IN_PROGRESS',
                'scheduled_date': date.today() + timedelta(days=1),
                'created_by': 'chief_engineer_s7000'
            },
            {
                'wo_id': 'WO-2024-005',
                'vessel_name': 'Saipem 7000',
                'machinery_serial': None,
                'asset_id': 'AST-004', # Helideck Safety System
                'description': 'Working at Height - Helideck Safety net and structure replacement',
                'priority': 'MEDIUM',
                'status': 'IN_PROGRESS',
                'scheduled_date': date.today(),
                'created_by': 'chief_engineer_s7000'
            },
            {
                'wo_id': 'WO-2024-006',
                'vessel_name': 'Saipem 7000',
                'machinery_serial': 'GEN-S7000-002', # Main Generator B
                'asset_id': None,
                'description': 'Electrical Isolation - Generator switchboard and Main Generator B maintenance',
                'priority': 'CRITICAL',
                'status': 'PENDING',
                'scheduled_date': date.today() + timedelta(days=5),
                'created_by': 'chief_engineer_s7000'
            },
            {
                'wo_id': 'WO-2024-007',
                'vessel_name': 'Saipem 7000',
                'machinery_serial': None,
                'asset_id': 'AST-001', # Main Crane
                'description': 'Scaffolding Erection - Access to Main Crane upper cabin equipment',
                'priority': 'MEDIUM',
                'status': 'PENDING',
                'scheduled_date': date.today() + timedelta(days=4),
                'created_by': 'chief_engineer_s7000'
            },
            {
                'wo_id': 'WO-2024-008',
                'vessel_name': 'Saipem 7000',
                'machinery_serial': None,
                'asset_id': 'AST-001', # Main Crane
                'description': 'Main Crane Inspection - Load testing and structural safety certification',
                'priority': 'CRITICAL',
                'status': 'PENDING',
                'scheduled_date': date.today() + timedelta(days=6),
                'created_by': 'chief_engineer_s7000'
            },
            {
                'wo_id': 'WO-2024-009',
                'vessel_name': 'Saipem 7000',
                'machinery_serial': 'GEN-S7000-001', # Main Generator A
                'asset_id': None,
                'description': 'Main Generator A Overhaul - Oil change, filter replacement, and valve check',
                'priority': 'HIGH',
                'status': 'PENDING',
                'scheduled_date': date.today() + timedelta(days=7),
                'created_by': 'chief_engineer_s7000'
            },
            {
                'wo_id': 'WO-2024-010',
                'vessel_name': 'Saipem 7000',
                'machinery_serial': None,
                'asset_id': 'AST-004', # Helideck Safety System
                'description': 'Helideck Safety Net Replacement - Guard rails and safety net installation',
                'priority': 'MEDIUM',
                'status': 'PENDING',
                'scheduled_date': date.today() + timedelta(days=3),
                'created_by': 'chief_engineer_s7000'
            },
            # Castorone
            {
                'wo_id': 'WO-2024-011',
                'vessel_name': 'Castorone',
                'machinery_serial': None,
                'asset_id': 'AST-002', # Auxiliary Crane
                'description': 'Auxiliary Crane Hydraulic Cylinder Repair - Seal replacement and system flush',
                'priority': 'HIGH',
                'status': 'PENDING',
                'scheduled_date': date.today() + timedelta(days=1),
                'created_by': 'chief_engineer_s7000'
            },
            {
                'wo_id': 'WO-2024-012',
                'vessel_name': 'Castorone',
                'machinery_serial': 'HPU-CAST-001', # Hydraulic Power Unit A
                'asset_id': None,
                'description': 'Hydraulic Power Unit A Maintenance - Overheating diagnostics and filter change',
                'priority': 'CRITICAL',
                'status': 'IN_PROGRESS',
                'scheduled_date': date.today(),
                'created_by': 'chief_engineer_s7000'
            },
            # Scarabeo 8
            {
                'wo_id': 'WO-2024-013',
                'vessel_name': 'Scarabeo 8',
                'machinery_serial': None,
                'asset_id': 'AST-009', # Blowout Preventer (BOP)
                'description': 'BOP Testing - Pressure testing of blowout preventer valves',
                'priority': 'CRITICAL',
                'status': 'PENDING',
                'scheduled_date': date.today() + timedelta(days=2),
                'created_by': 'chief_engineer_s7000'
            },
            {
                'wo_id': 'WO-2024-014',
                'vessel_name': 'Scarabeo 8',
                'machinery_serial': 'PMP-SCAR-001', # Drill Mud Pump A
                'asset_id': None,
                'description': 'Drill Mud Pump A Overhaul - Seal inspection and impeller replacement',
                'priority': 'HIGH',
                'status': 'IN_PROGRESS',
                'scheduled_date': date.today(),
                'created_by': 'chief_engineer_s7000'
            }
        ]

        for wo_data in work_orders_data:
            try:
                vessel = vessels[wo_data['vessel_name']]
                
                asset = None
                if wo_data['asset_id']:
                    asset = Asset.objects.get(asset_id=wo_data['asset_id'])
                
                machinery = None
                if wo_data['machinery_serial']:
                    machinery = MachineryEquipment.objects.get(serial_number=wo_data['machinery_serial'])
                
                wo, created = WorkOrder.objects.get_or_create(
                    wo_id=wo_data['wo_id'],
                    defaults={
                        'vessel': vessel,
                        'asset': asset,
                        'machinery': machinery,
                        'description': wo_data['description'],
                        'priority': wo_data['priority'],
                        'status': wo_data['status'],
                        'scheduled_date': wo_data['scheduled_date'],
                        'created_by': wo_data['created_by']
                    }
                )
                if created:
                    self.stdout.write(f"✓ Created work order: {wo.wo_id} ({wo.priority}) on {vessel.vessel_name}")
                else:
                    self.stdout.write(f"- Work order already exists: {wo.wo_id}")
            except (KeyError, Asset.DoesNotExist, MachineryEquipment.DoesNotExist) as e:
                self.stdout.write(self.style.WARNING(f"⚠ Error creating work order {wo_data['wo_id']}: {str(e)}"))

        self.stdout.write(f"\n✓ Total work orders: {WorkOrder.objects.count()}")

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
        self.stdout.write(f"✓ Machinery Equipment: {MachineryEquipment.objects.count()}")
        self.stdout.write(f"✓ Work Orders: {WorkOrder.objects.count()}")
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("🚀 Ready for testing!"))
