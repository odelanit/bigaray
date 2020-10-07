from django.contrib import admin
from django.db import models
from django.utils.crypto import get_random_string

from backend.models import Site


def scraper_path(instance, filename):
    name = get_random_string(length=16)
    return "scrapers/{0}.py".format(name)


def validate_py_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.py']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class Scraper(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    file = models.FileField(upload_to=scraper_path, null=True, validators=[validate_py_extension])

    is_active = models.BooleanField()
    last_scraped = models.DateTimeField()


class ScraperAdmin(admin.ModelAdmin):
    list_display = ('site', 'is_active', 'start_time', 'end_time', 'last_scraped',)
    readonly_fields = ('last_scraped',)


class ScraperLog(models.Model):
    scraper = models.ForeignKey(Scraper, on_delete=models.SET_NULL, null=True)
