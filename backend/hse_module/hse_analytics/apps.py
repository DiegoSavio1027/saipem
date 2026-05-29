from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class HseAnalyticsConfig(AppConfig):
    name = 'hse_module.hse_analytics'
    verbose_name = 'HSE Analytics'

    def ready(self):
        """
        Start the analytics scheduler when Django app is ready
        """
        try:
            from .scheduler import start_scheduler, is_scheduler_running

            # Only start if not already running
            if not is_scheduler_running():
                start_scheduler()
                logger.info("Analytics scheduler initialized")
        except Exception as e:
            logger.error(f"Failed to initialize analytics scheduler: {str(e)}")

