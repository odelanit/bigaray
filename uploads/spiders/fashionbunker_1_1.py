import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Fashionbunker_1_1'  # name_gender_type
    allowed_domains = ['us.fashionbunker.com']
    start_urls = ['https://us.fashionbunker.com/new-arrivals?p=%s' % page for page in range(1, 54)]

    def parse(self, response, **kwargs):
        if 200 <= response.status <= 209:
            products = response.css('.products > li.product-item')
            for idx, product in enumerate(products):
                item = ProductItem()
                title = product.css('.product-item-link::text').get()
                if title:
                    item['title'] = title.strip()
                else:
                    continue
                price = product.css('span.price::text').get()
                if price:
                    item['price'] = price
                else:
                    continue

                image_url = product.css('img::attr(data-src)').get()
                if image_url:
                    item['image_urls'] = [image_url, image_url]
                else:
                    continue

                product_link = product.css('.product-item-link::attr(href)').get()
                item['product_link'] = product_link
                yield item
