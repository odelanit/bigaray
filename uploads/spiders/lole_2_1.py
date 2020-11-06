import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Lole_2_1'  # name_gender_type
    allowed_domains = ['www.lolelife.com']
    base_url = 'https://www.lolelife.com'
    start_urls = [
        'https://www.lolelife.com/men/new-arrivals'
    ]

    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def parse(self, response, **kwargs):
        products = response.css('.cy-product-block')
        for product in products:
            item = ProductItem()
            title = product.css('.title-product > h2::text').get()
            if title:
                item['title'] = title.strip()
            else:
                continue
            product_link = product.css('a::attr(href)').get()
            price = product.css('.amount span:last-child::text').get()
            if price:
                item['price'] = "${0}".format(price)
            else:
                continue
            image_srcset = product.css('img::attr(data-srcset)').get()
            image_urls = image_srcset.split(',')
            image_url = image_urls[0].split(' ')[0].replace('/50/', '/400/')
            hq_image_url = image_url.replace('/400/', '/800/')
            item['image_urls'] = [image_url, hq_image_url]
            item['product_link'] = "{0}{1}".format(self.base_url, product_link)
            yield item
        # with open('lole.html', 'w', encoding='utf8') as html_file:
        #     html_file.write(response.text)
