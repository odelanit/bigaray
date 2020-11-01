import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Diesel_2_1'  # name_gender_type
    allowed_domains = ['ca.diesel.com']
    root_path = 'https://ca.diesel.com'
    start_urls = [
        'https://ca.diesel.com/en/shop-man-latest-arrivals/',
        'https://ca.diesel.com/en/shop-man-latest-arrivals/?lang=en&cgid=diesel-woman-features-latestarrivals&start=46&sz=46',
        'https://ca.diesel.com/en/shop-man-latest-arrivals/?lang=en&cgid=diesel-woman-features-latestarrivals&start=106&sz=60'
    ]

    def parse(self, response, **kwargs):
        products = response.css('.js_tile')
        for idx, product in enumerate(products):
            item = ProductItem()
            item['title'] = product.css('.product-link::text').get()
            price = product.css('span[itemprop="price"]::text').get()
            if price:
                item['price'] = price.strip()
            else:
                continue

            image_url = product.css('img::attr(data-src)').get()
            if image_url:
                b = image_url.split('.jpg?')
                c = b[1]
                d = c.split('&')
                sw = int((d[0].split("sw="))[1])
                sh = int((d[1].split("sh="))[1])
                hq_image_url = "{0}.jpg?sw={1}&sh={2}".format(b[0], sw * 2, sh * 2)
                item['image_urls'] = [image_url, hq_image_url]
            else:
                continue

            product_link = product.css('.product-link::attr(href)').get()
            item['product_link'] = self.root_path + product_link
            yield item
