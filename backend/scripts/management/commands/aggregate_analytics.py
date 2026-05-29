from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from hse_module.hse_analytics.services import (
    aggregate_all_analytics,
    calculate_safety_metrics,
    calculate_location_statistics,
    calculate_incident_trends
)


class Command(BaseCommand):
    help = 'Manually trigger analytics data aggregation from operational data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Specific date to aggregate (YYYY-MM-DD format). Default: today'
        )
        parser.add_argument(
            '--days-back',
            type=int,
            default=30,
            help='Number of days to aggregate backwards. Default: 30'
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['all', 'metrics', 'locations', 'trends'],
            default='all',
            help='Type of analytics to aggregate. Default: all'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting analytics aggregation...'))

        # Parse target date
        if options['date']:
            try:
                target_date = datetime.strptime(options['date'], '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.ERROR('Invalid date format. Use YYYY-MM-DD'))
                return
        else:
            target_date = timezone.now().date()

        days_back = options['days_back']
        agg_type = options['type']

        try:
            if agg_type == 'all':
                # Aggregate all analytics
                self.stdout.write('Aggregating all analytics data...')
                aggregate_all_analytics()
                self.stdout.write(self.style.SUCCESS('✓ All analytics aggregated successfully'))

            elif agg_type == 'metrics':
                # Aggregate safety metrics
                self.stdout.write(f'Aggregating safety metrics for {target_date}...')
                calculate_safety_metrics(target_date)
                self.stdout.write(self.style.SUCCESS(f'✓ Safety metrics aggregated for {target_date}'))

            elif agg_type == 'locations':
                # Aggregate location statistics
                self.stdout.write(f'Aggregating location statistics for {target_date}...')
                calculate_location_statistics(target_date)
                self.stdout.write(self.style.SUCCESS(f'✓ Location statistics aggregated for {target_date}'))

            elif agg_type == 'trends':
                # Aggregate incident trends
                self.stdout.write(f'Aggregating incident trends (last {days_back} days)...')
                calculate_incident_trends('DAILY', days_back=days_back)
                calculate_incident_trends('WEEKLY')
                calculate_incident_trends('MONTHLY')
                self.stdout.write(self.style.SUCCESS('✓ Incident trends aggregated'))

            self.stdout.write(self.style.SUCCESS('\n✓ Analytics aggregation completed successfully!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error during aggregation: {str(e)}'))
            raise
