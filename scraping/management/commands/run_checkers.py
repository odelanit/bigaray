from django.core.management import BaseCommand

from scraping.models import Scraper, ProductChecker


class Command(BaseCommand):
    help = "run all checkers"

    def handle(self, *args, **options):
        checkers = ProductChecker.objects.all()
        for checker in checkers:
            checker.start()
