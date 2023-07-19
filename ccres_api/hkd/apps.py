from django.apps import AppConfig


class HkdConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hkd"

    def ready(self):
        import hkd.signals.create_dashboards  # noqa
        import hkd.signals.create_contact  # noqa
        import hkd.signals.create_alerts  # noqa
