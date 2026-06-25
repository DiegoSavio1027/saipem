from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from auth_module.models import UserProfile
from asset_module.models import Vessel, WorkOrder
from hse_module.hse_pob.models import WorkLocation
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Seed complete HSE system data: users, profiles, work orders, and locations'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("SAIPEM HSE - Complete Data Seeder")
        self.stdout.write("=" * 60)

        # STEP 1: Create groups
        self.stdout.write('\n[1/5] Creating User Groups...')
        groups_data = [
            'Admin',
            'HR Staff',
            'Chief Engineer',
            'Worker',
            'Safety Officer',
        ]

        for group_name in groups_data:
            Group.objects.get_or_create(name=group_name)
            self.stdout.write(self.style.SUCCESS(f'✓ Group "{group_name}" created/exists'))

        # STEP 2: Create test users with UserProfile data
        self.stdout.write('\n[2/5] Creating Users and Profiles...')
        test_users = [
            {
                'username': 'chief_engineer_hq',
                'password': 'chief123',
                'email': 'chief_hq@saipem.com',
                'first_name': 'Johan',
                'last_name': 'HQ',
                'is_superuser': False,
                'group': 'Chief Engineer',
                'job_role': 'Chief Engineer',
                'roster_status': 'AVAILABLE'
            },
            {
                'username': 'chief_engineer_castorone',
                'password': 'chief123',
                'email': 'chief_castorone@saipem.com',
                'first_name': 'Johan',
                'last_name': 'Castorone',
                'is_superuser': False,
                'group': 'Chief Engineer',
                'job_role': 'Chief Engineer',
                'roster_status': 'ONBOARD'
            },
            {
                'username': 'safety_officer_hq',
                'password': 'safety123',
                'email': 'safety_hq@saipem.com',
                'first_name': 'Diego',
                'last_name': 'HQ',
                'is_superuser': False,
                'group': 'Safety Officer',
                'job_role': 'Safety Officer',
                'roster_status': 'AVAILABLE'
            },
            {
                'username': 'safety_officer_castorone',
                'password': 'safety123',
                'email': 'safety_castorone@saipem.com',
                'first_name': 'Diego',
                'last_name': 'Castorone',
                'is_superuser': False,
                'group': 'Safety Officer',
                'job_role': 'Safety Officer',
                'roster_status': 'ONBOARD'
            },

            {
                'username': 'admin',
                'password': 'admin123',
                'email': 'admin@saipem.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_superuser': True,
                'group': 'Admin',
                'job_role': 'System Administrator',
                'roster_status': 'AVAILABLE'
            },
            {
                'username': 'hr_staff',
                'password': 'hr123',
                'email': 'hr@saipem.com',
                'first_name': 'Ijlal',
                'last_name': 'Nuhlan',
                'is_superuser': False,
                'group': 'HR Staff',
                'job_role': 'HR Staff',
                'roster_status': 'AVAILABLE'
            },
            {
                'username': 'chief_engineer_s7000',
                'password': 'chief123',
                'email': 'chief@saipem.com',
                'first_name': 'Johan',
                'last_name': 'Branson',
                'is_superuser': False,
                'group': 'Chief Engineer',
                'job_role': 'Chief Engineer',
                'roster_status': 'ONBOARD'
            },
            {
                'username': 'worker',
                'password': 'worker123',
                'email': 'worker@saipem.com',
                'first_name': 'Aron',
                'last_name': 'Piper',
                'is_superuser': False,
                'group': 'Worker',
                'job_role': 'Worker',
                'roster_status': 'ONBOARD'
            },
            {
                'username': 'safety_officer_s7000',
                'password': 'safety123',
                'email': 'safety@saipem.com',
                'first_name': 'Diego',
                'last_name': 'Savio',
                'is_superuser': False,
                'group': 'Safety Officer',
                'job_role': 'Safety Officer',
                'roster_status': 'ONBOARD'
            },
            {
                'username': 'worker_off',
                'password': 'worker123',
                'email': 'workeroff@saipem.com',
                'first_name': 'Raf',
                'last_name': 'Simons',
                'is_superuser': False,
                'group': 'Worker',
                'job_role': 'Worker',
                'roster_status': 'AVAILABLE'
            },
        ]

        for user_data in test_users:
            username = user_data['username']
            try:
                user = User.objects.get(username=username)
                user.first_name = user_data['first_name']
                user.last_name = user_data['last_name']
                user.email = user_data['email']
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Updated existing user {username}'))
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=user_data['username'],
                    password=user_data['password'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    is_superuser=user_data['is_superuser']
                )

                # Assign user to group
                group = Group.objects.get(name=user_data['group'])
                user.groups.add(group)

                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created user {username} with group {user_data["group"]}'
                    )
                )

            # Update UserProfile (auto-created by signal)
            if hasattr(user, 'profile'):
                user.profile.job_role = user_data['job_role']
                user.profile.roster_status = user_data['roster_status']
                user.profile.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Updated profile for {username}')
                )

        # STEP 3: Get or create default Vessel for Work Orders
        self.stdout.write('\n[3/5] Ensuring default Vessel exists...')
        default_vessel, created = Vessel.objects.get_or_create(
            vessel_name='Saipem 7000',
            defaults={
                'vessel_type': 'Drill Ship',
                'imo_number': 'IMO-7000-001',
                'operational_status': 'OPERATIONAL',
                'health_score': 95
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created default vessel: {default_vessel.vessel_name}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✓ Using existing vessel: {default_vessel.vessel_name}'))

        # STEP 4: Create Work Locations (Deck Locations - linked to Vessel)
        self.stdout.write('\n[4/4] Creating Deck Locations...')
        locations_data = [
            {'deck_name': 'Main Deck', 'risk_level': 'MEDIUM'},
            {'deck_name': 'Engine Room', 'risk_level': 'HIGH'},
            {'deck_name': 'Heli Deck', 'risk_level': 'MEDIUM'},
            {'deck_name': 'Lower Deck', 'risk_level': 'LOW'},
            {'deck_name': 'Upper Deck', 'risk_level': 'MEDIUM'},
            {'deck_name': 'Machinery Space', 'risk_level': 'HIGH'},
        ]

        for loc_data in locations_data:
            location, created = WorkLocation.objects.get_or_create(
                deck_name=loc_data['deck_name'],
                defaults={'risk_level': loc_data['risk_level']}
            )
            if created:
                self.stdout.write(f"✓ Created deck location: {location.deck_name} (Risk: {location.risk_level})")
                # Assign the location to the default vessel
                default_vessel.assigned_decks.add(location)
            else:
                self.stdout.write(f"- Deck location already exists: {location.deck_name}")
                # Ensure it's assigned to the default vessel
                if location not in default_vessel.assigned_decks.all():
                    default_vessel.assigned_decks.add(location)

        self.stdout.write(self.style.SUCCESS('\n✓ All data seeded successfully!'))
