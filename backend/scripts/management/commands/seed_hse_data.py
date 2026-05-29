from django.core.management.base import BaseCommand
from hse_module.hse_safety.models import SystemStatus


class Command(BaseCommand):
    help = 'Initialize HSE Safety system with default SystemStatus'

    def handle(self, *args, **options):
        system_status, created = SystemStatus.get_or_create_singleton()

        if created:
            self.stdout.write(
                self.style.SUCCESS('✓ SystemStatus initialized successfully')
            )
            self.stdout.write(f'  Global Status: {system_status.global_status}')
            self.stdout.write(f'  Days Without LTI: {system_status.days_without_lti}')
            self.stdout.write(f'  Near Misses Count: {system_status.near_misses_count}')
            self.stdout.write(f'  Active Permits: {system_status.active_permits}')
        else:
            self.stdout.write(
                self.style.WARNING('⚠ SystemStatus already exists')
            )
            self.stdout.write(f'  Global Status: {system_status.global_status}')
            self.stdout.write(f'  Days Without LTI: {system_status.days_without_lti}')
            self.stdout.write(f'  Near Misses Count: {system_status.near_misses_count}')
            self.stdout.write(f'  Active Permits: {system_status.active_permits}')
