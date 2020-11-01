import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Urban-outfitters_2_2'  # name_gender_type
    allowed_domains = ['www.urbanoutfitters.com']
    start_urls = [
        'https://www.urbanoutfitters.com/womens-clothing-sale?page=%s' % page for page in range(1, 17)
    ]
    custom_settings = {
        "DOWNLOAD_DELAY": 20
    }
    base_url = "https://www.urbanoutfitters.com"

    def parse(self, response, **kwargs):
        products = response.css('.c-pwa-tile-grid-inner')
        for idx, product in enumerate(products):
            product_link = product.css('a.c-pwa-product-tile__link::attr(href)').get()
            if product_link:
                absolute_url = self.base_url + product_link
                yield scrapy.Request(absolute_url, callback=self.parse_product)
            else:
                continue

    def parse_product(self, response):
        item = ProductItem()
        item['product_link'] = response.request.url
        title = response.css('.c-pwa-product-meta-heading::text').get()
        if title:
            item['title'] = title.strip()
        else:
            pass
        sale_price = response.css('span.c-pwa-product-price__current::text').get()
        if sale_price:
            item['sale_price'] = sale_price
        else:
            pass
        price = response.css('span.c-pwa-product-price__original::text').get()
        if price:
            item['price'] = price
        else:
            pass
        hq_image_url = response.css('img.c-pwa-image-viewer__img::attr(src)').get()
        image_url = hq_image_url.replace('wid=683', 'wid=400')
        if hq_image_url:
            item['image_urls'] = [image_url, hq_image_url]
        else:
            pass
        yield item
