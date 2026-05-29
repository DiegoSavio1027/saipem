from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

scheduler = None


def start_scheduler():
    """
    Start the background scheduler for analytics aggregation
    """
    global scheduler

    if scheduler is not None and scheduler.running:
        logger.info("Scheduler is already running")
        return

    try:
        scheduler = BackgroundScheduler()

        # Import here to avoid circular imports
        from .services import aggregate_all_analytics

        # Schedule analytics aggregation
        # Run every day at 1:00 AM (01:00)
        scheduler.add_job(
            aggregate_all_analytics,
            trigger=CronTrigger(hour=1, minute=0),
            id='aggregate_analytics_daily',
            name='Daily Analytics Aggregation',
            replace_existing=True,
            max_instances=1
        )

        # Also run every 6 hours for more frequent updates
        scheduler.add_job(
            aggregate_all_analytics,
            trigger=CronTrigger(hour='*/6'),
            id='aggregate_analytics_6hourly',
            name='6-Hourly Analytics Aggregation',
            replace_existing=True,
            max_instances=1
        )

        scheduler.start()
        logger.info("Analytics scheduler started successfully")

    except Exception as e:
        logger.error(f"Failed to start analytics scheduler: {str(e)}")
        raise


def stop_scheduler():
    """
    Stop the background scheduler
    """
    global scheduler

    if scheduler is not None and scheduler.running:
        scheduler.shutdown()
        scheduler = None
        logger.info("Analytics scheduler stopped")


def get_scheduler():
    """
    Get the current scheduler instance
    """
    return scheduler


def is_scheduler_running():
    """
    Check if scheduler is running
    """
    return scheduler is not None and scheduler.running
