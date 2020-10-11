import os

from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from uploads.spiders.allsaints import ProductSpider


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        settings_file_path = "scraping.spiders.settings"
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        settings = get_project_settings()
        process = CrawlerProcess(settings)

        process.crawl(ProductSpider)
        process.start()
