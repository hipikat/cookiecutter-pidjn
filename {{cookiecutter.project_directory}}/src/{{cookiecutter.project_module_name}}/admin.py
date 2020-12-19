from django.contrib import admin
from cms.extensions import PageExtensionAdmin

from .models import SeriesExtension


class SeriesExtensionAdmin(PageExtensionAdmin):
        pass

admin.site.register(SeriesExtension, SeriesExtensionAdmin)
