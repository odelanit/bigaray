import json

import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Ted-baker_2_1'  # name_gender_type
    allowed_domains = ['www.tedbaker.com']
    base_url = 'https://www.tedbaker.com'
    start_urls = [
        'https://www.tedbaker.com/ca/json/c/mens_clothing_new-arrivals?show=ALL&slotsToSave=1'
    ]

    def start_requests(self):
        for url in self.start_urls:
            proxy = 'http://191.102.232.130:3128'
            yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': proxy})

    def parse(self, response, **kwargs):
        json_response = json.loads(response.body)
        success = json_response.get('success')
        if success:
            products = json_response.get('data').get('results')
            for product in products:
                item = ProductItem()
                item['title'] = product.get('name')
                item['price'] = "{0} {1}".format(product.get('price').get('currencyIso'), product.get('price').get('value'))
                primary_image_url = product.get('primaryImage').get('url')
                image_url = primary_image_url.replace(
                    'https://media.tedbaker.com/', 'https://media.tedbaker.com/t_lgd_plp_primary,q_auto:best,f_auto/'
                )
                hq_image_url = primary_image_url.replace(
                    'https://media.tedbaker.com/', 'https://media.tedbaker.com/t_lgd_landscape_double_width,q_auto:best,f_auto/'
                )
                item['image_urls'] = [
                    image_url,
                    hq_image_url,
                ]

                item['product_link'] = self.base_url + product.get('url')
                yield item
