import bigaray.settings

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Import spiders from uploads folder."

    def handle(self, *args, **options):
        pass
