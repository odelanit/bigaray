import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Allsaints_1_2'
    allowed_domains = ['www.ca.allsaints.com']
    domain = 'https://www.ca.allsaints.com'
    start_urls = ['https://www.ca.allsaints.com/women/outlet-store/style,any/colour,any/size,any/?page=%s' % page for page in range(1, 8)]

    def start_requests(self):
        for url in self.start_urls:
            proxy = 'http://191.102.232.130:3128'
            yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': proxy})

    def parse(self, response, **kwargs):
        if 200 <= response.status <= 209:
            products = response.css('div.product-item')
            for idx, product in enumerate(products):
                item = ProductItem()
                item['title'] = product.css('span.product-item__name__text::text').get()
                item['price'] = product.css('span.product-item__price-old::text').get().strip()
                item['sale_price'] = product.css('span.product-item__price-new::text').get().strip()
                image_url = product.css('img::attr(src)').get()
                if 'https:' not in image_url:
                    image_url = 'https:' + image_url
                b = image_url.split('https://images.allsaints.com/products/')
                c = b[1].split('/')
                hq_image_url = "https://images.allsaints.com/products/900"
                for i, x in enumerate(c):
                    if i != 0:
                        hq_image_url = "{0}/{1}".format(hq_image_url, x)
                item['image_urls'] = [image_url, hq_image_url]
                # TODO: image_filename, sale_price, hq_image_filename
                product_link = product.css('a.mainImg::attr(href)').get()
                item['product_link'] = self.domain + product_link
                yield item
