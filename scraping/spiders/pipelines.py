# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from backend.models import Site, Product


class ProductPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        site_name_gender_type = spider.name
        site_keys = site_name_gender_type.split('_')
        site_name = site_keys[0]
        site_gender = site_keys[1]
        site_type = site_keys[2]
        try:
            site = Site.objects.get(name=site_name, gender=site_gender, type=site_type)
            title = adapter.get('title')
            price = adapter.get('price')
            sale_price = adapter.get('sale_price')
            images = adapter.get('images')
            image_filename = None
            hq_image_filename = None
            if len(images) == 1:
                image_filename = images[0].get('path')
                hq_image_filename = None
            elif len(images) == 2:
                image_filename = images[0].get('path')
                hq_image_filename = images[1].get('path')
            product_link = adapter.get('product_link')
            try:
                product = Product.objects.get(site=site, product_link=product_link)
                product.price = price
                product.sale_price = sale_price
                product.image_filename = image_filename
                product.hq_image_filename = hq_image_filename
                product.product_link = product_link
                product.save()
                print("Product: {} updated.".format(title))
            except Product.DoesNotExist:
                Product.objects.create(
                    title=title,
                    price=price, sale_price=sale_price,
                    image_filename=image_filename, hq_image_filename=hq_image_filename,
                    product_link=product_link, site=site
                )
                print("Product: {} added.".format(title))
        except Site.DoesNotExist:
            print("{} does not exist".format(site_name_gender_type))
        return item
