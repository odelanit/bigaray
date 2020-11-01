import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Freepeople_1_2'  # name_gender_type
    allowed_domains = ['www.freepeople.com']
    root_url = 'https://www.freepeople.com'
    start_urls = ['https://www.freepeople.com/sale-all/?page=%s' % page for page in range(1, 7)]
    custom_settings = {
        "DOWNLOAD_DELAY": 20
    }

    def parse(self, response, **kwargs):
        if 200 <= response.status <= 209:
            products = response.css('.c-pwa-product-tile')
            for idx, product in enumerate(products):
                item = ProductItem()
                title = product.css('.c-pwa-product-tile__heading::text').get()
                if title:
                    item['title'] = title.strip()
                else:
                    continue
                sale_price = product.css('span.c-pwa-product-price__current::text').get()
                if sale_price:
                    item['sale_price'] = sale_price
                else:
                    continue

                price = product.css('span.c-pwa-product-price__original::text').get()
                if price:
                    item['price'] = price
                else:
                    continue

                image_src_set = product.css('source::attr(srcset)').get()
                if image_src_set:
                    b = image_src_set.split(', ')
                    c = b[0].split(' 698w')
                    d = b[1].split(' 349w')
                    image_url = d[0]
                    hq_image_url = c[0]
                    item['image_urls'] = [image_url, hq_image_url]
                else:
                    continue

                product_link = product.css('.c-pwa-product-tile__link::attr(href)').get()
                item['product_link'] = self.root_url + product_link
                yield item
