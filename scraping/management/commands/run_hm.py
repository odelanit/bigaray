from django.core.management import BaseCommand

from scraping.models import Scraper


class Command(BaseCommand):
    help = "crawl Hm_1_1"

    def handle(self, *args, **options):
        scraper = Scraper.objects.get(id=54)
        scraper.start()
