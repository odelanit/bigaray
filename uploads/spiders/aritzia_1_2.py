import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Aritzia_1_2'  # name_gender_type
    allowed_domains = ['www.aritzia.com']
    start_urls = ['https://www.aritzia.com/us/en/sale?start=0&sz=10000&loadmore=true']

    def parse(self, response, **kwargs):
        products = response.css('.product-tile')
        for idx, product in enumerate(products):
            item = ProductItem()
            brand_name = product.css('.product-brand > h6 > a::text').get()
            product_name = product.css('.product-name > h6 > a::text').get()
            item['title'] = "{0} {1}".format(brand_name, product_name)
            item['price'] = product.css('.ar-product__price-single > span > span::text').get()
            item['sale_price'] = product.css('.js-product__sales-price > span::text').get()
            image_url = product.css('.product-image > a > img::attr(data-original)').get()
            item['image_urls'] = [image_url, image_url]
            product_link = product.css('a::attr(href)').get()
            item['product_link'] = product_link
            yield item
