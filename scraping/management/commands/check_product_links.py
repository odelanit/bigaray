import os

from django.core.management import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraping.spiders.spiders import BrokenLinksSpider


class Command(BaseCommand):
    def handle(self, *args, **options):
        # settings_file_path = "scraping.spiders.settings"
        # os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        # settings = get_project_settings()
        # process = CrawlerProcess(settings)
        process = CrawlerProcess()

        process.crawl(BrokenLinksSpider)
        process.start()
