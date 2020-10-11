import os
from pydoc import locate

from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraping.models import Scraper


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        settings_file_path = "scraping.spiders.settings"
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        settings = get_project_settings()
        process = CrawlerProcess(settings)

        spider = Scraper.objects.get(id=3)
        url = spider.file.name
        url = url.replace('.py', '')
        url = url.replace('/', '.')
        file_path = "uploads.{0}.ProductSpider".format(url)

        ProductSpider = locate(file_path)

        process.crawl(ProductSpider)
        process.start()
        # pass
