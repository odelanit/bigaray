import os
from pydoc import locate

from django.contrib import admin
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.timezone import now
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

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
    description = models.TextField(null=True)
    file = models.FileField(upload_to=scraper_path, null=True, validators=[validate_py_extension])

    # is_active = models.BooleanField()
    last_scraped = models.DateTimeField(null=True)

    def start(self):
        settings_file_path = "scraping.spiders.settings"
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        settings = get_project_settings()
        runner = CrawlerRunner(settings)

        url = self.file.name
        url = url.replace('.py', '')
        url = url.replace('/', '.')
        file_path = "uploads.{0}.ProductSpider".format(url)

        ProductSpider = locate(file_path)

        d = runner.crawl(ProductSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()


class ScraperAdmin(admin.ModelAdmin):
    list_display = ('id', 'site', 'file', 'last_scraped', 'site_actions',)
    readonly_fields = ('last_scraped', 'site_actions',)

    def start_scraping(self, request, object_id, *args, **kwargs):
        scraper = self.get_object(request, object_id)
        scraper.start()
        scraper.last_scraped = now()
        scraper.save()
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
