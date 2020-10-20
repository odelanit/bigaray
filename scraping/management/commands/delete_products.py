from django.core.management import BaseCommand

from backend.models import Product


class Command(BaseCommand):
    help = "Delete products having empty image field"

    def handle(self, *args, **options):
        products = Product.objects.filter(image_filename__isnull=True)
        products.delete()
        print('Successfully Deleted')
