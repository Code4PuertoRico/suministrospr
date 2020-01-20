from django.apps import AppConfig


class SuministrosConfig(AppConfig):
    name = "suministrospr.suministros"
    verbose_name = "suministros"

    def ready(self):
        from . import signals  # noqa
