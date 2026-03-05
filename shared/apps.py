from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SharedConfig(AppConfig):
    name = 'shared'
    verbose_name = _('shared')