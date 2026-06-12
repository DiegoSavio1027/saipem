from django.apps import AppConfig


class AssetModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'asset_module'

    def ready(self):
        import asset_module.signals
