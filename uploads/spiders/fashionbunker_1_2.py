import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Fashionbunker_1_2'  # name_gender_type
    allowed_domains = ['us.fashionbunker.com']
    start_urls = ['https://us.fashionbunker.com/sale?p=%s' % page for page in range(1, 31)]

    def parse(self, response, **kwargs):
        products = response.css('.products > li.product-item')
        for idx, product in enumerate(products):
            item = ProductItem()
            title = product.css('.product-item-link::text').get()
            if title:
                item['title'] = title.strip()
            else:
                continue
            price = product.css('span[data-price-type="oldPrice"] > span.price::text').get()
            if price:
                item['price'] = price
            else:
                continue

            sale_price = product.css('span[data-price-type="finalPrice"] > span.price::text').get()
            if sale_price:
                item['sale_price'] = sale_price
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
