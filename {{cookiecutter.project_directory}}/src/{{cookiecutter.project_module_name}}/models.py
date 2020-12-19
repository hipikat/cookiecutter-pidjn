
from django.db import models
from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool


class SeriesExtension(PageExtension):
        # TODO: make max_length(s) configurable
        series = models.CharField(max_length=256)
        series_part_index = models.PositiveSmallIntegerField()
        series_part_label = models.CharField(max_length=64)

extension_pool.register(SeriesExtension)
