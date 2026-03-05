from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogsConfig(AppConfig):
    name = 'blogs'
    verbose_name = _('blogs')
