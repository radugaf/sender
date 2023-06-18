from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BrainConfig(AppConfig):
    name = "sender.brain"
    verbose_name = _("Brain")

    def ready(self):
        try:
            import sender.brain.signals  # noqa: F401
        except ImportError:
            pass
