from django.apps import AppConfig


class HsePtwConfig(AppConfig):
    name = 'hse_module.hse_ptw'

    def ready(self):
        import hse_module.hse_ptw.signals
