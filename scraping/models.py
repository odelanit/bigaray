from django.contrib import admin
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import redirect
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.timezone import now
from scrapyd_api import ScrapydAPI

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
    # start_time = models.TimeField(null=True)
    # end_time = models.TimeField(null=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=scraper_path, null=True, validators=[validate_py_extension])
    task_id = models.CharField(null=True, blank=True)

    # is_active = models.BooleanField()
    last_scraped = models.DateTimeField(null=True)

    class Meta:
        ordering = ['site__name']

    def start(self):
        scrapyd = ScrapydAPI("http://localhost:6800")
        spider_name = "{}_{}_{}".format(self.site.name, self.site.gender, self.site.type)
        self.task_id = scrapyd.schedule("default", spider_name)
        self.save()
        pass


@receiver(post_delete, sender=Scraper)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)


class ScraperAdmin(admin.ModelAdmin):
    list_display = ('id', 'site', 'file', 'last_scraped', 'task_id', 'site_actions',)
    readonly_fields = ('last_scraped', 'task_id', 'site_actions',)

    def start_scraping(self, request, object_id, *args, **kwargs):
        scraper = self.get_object(request, object_id)
        scraper.last_scraped = now()
        scraper.save()
        scraper.start()
        return redirect(request.META['HTTP_REFERER'])

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/start/', self.admin_site.admin_view(self.start_scraping),
                 name='scraping_scraper_start')
        ]
        return custom_urls + urls

    def site_actions(self, obj):
        return format_html('<a class="el-button" href={}>Start</a>',
                           reverse('admin:scraping_scraper_start', kwargs={'object_id': obj.pk})
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
