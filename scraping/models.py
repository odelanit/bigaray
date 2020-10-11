from django.contrib import admin
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse, path
from django.utils.html import format_html

from backend.models import Site


def scraper_path(instance, filename):
    return "spiders/{0}".format(filename)


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
    description = models.TextField(null=True)
    file = models.FileField(upload_to=scraper_path, null=True, validators=[validate_py_extension])

    is_active = models.BooleanField()
    last_scraped = models.DateTimeField(null=True)

    def toggle_status(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()


class ScraperAdmin(admin.ModelAdmin):
    list_display = ('site', 'is_active', 'start_time', 'end_time', 'last_scraped', 'site_actions',)
    readonly_fields = ('last_scraped', 'site_actions',)

    def toggle_status(self, request, object_id, *args, **kwargs):
        site = self.get_object(request, object_id)
        site.toggle_status()
        return redirect(request.META['HTTP_REFERER'])

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/status/', self.admin_site.admin_view(self.toggle_status), name='scraping_scraper_toggle_active')
        ]
        return custom_urls + urls

    def site_actions(self, obj):
        if obj.is_active:
            name = 'Stop'
        else:
            name = 'Start'
        return format_html('<a class="el-button" href={}>{}</a>',
                           reverse('admin:scraping_scraper_toggle_active', kwargs={'object_id': obj.pk}),
                           name
                           )

    site_actions.short_description = "Change Status"
    site_actions.allow_tags = True


class ScraperLog(models.Model):
    scraper = models.ForeignKey(Scraper, on_delete=models.SET_NULL, null=True)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    description = models.TextField(null=True)


class ScraperLogAdmin(admin.ModelAdmin):
    list_display = ('scraper', 'started_at', 'finished_at')
    readonly_fields = ('scraper', 'started_at', 'finished_at')
