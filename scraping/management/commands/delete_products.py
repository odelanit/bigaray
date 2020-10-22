from django.core.management import BaseCommand
from django.db.models import Q

from backend.models import Product


class Command(BaseCommand):
    help = "Delete products having empty image field"

    def handle(self, *args, **options):
        products = Product.objects.filter(Q(image_filename__isnull=True) | Q(product_link__isnull=True))
        products.delete()
        print('Successfully Deleted')
