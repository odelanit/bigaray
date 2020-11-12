import time

import scrapy
from django.utils import timezone
from parsel import Selector
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from scraping.models import Scraper
from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Hm_1_2'  # name_gender_type
    allowed_domains = ['www2.hm.com']
    start_urls = [
        'https://www2.hm.com/en_ca/sale/shopbyproductladies/view-all.html?sort=stock&image-size=small&image=model&offset=%s&page-size=80' % offset
        for offset in range(0, 900, 300)
    ]
    base_url = 'https://www2.hm.com'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ProductSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider, reason):
        a = spider.name.split('_')
        try:
            scraper = Scraper.objects.get(site__name=a[0], site__gender=int(a[1]), site__type=int(a[2]))
            scraper.last_scraped = timezone.now()
            scraper.save()
        except Scraper.DoesNotExist:
            pass

    def scroll(self, browser, timeout):
        scroll_pause_time = timeout
        position = 0
        step = 1000

        time.sleep(scroll_pause_time)

        while True:
            position = position + step
            browser.execute_script("window.scrollTo(0, {0});".format(position))

            time.sleep(scroll_pause_time)

            document_height = browser.execute_script("return document.body.scrollHeight")
            if document_height < position:
                break

    def parse(self, response, **kwargs):
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options)
        # browser = webdriver.Firefox()
        browser.implicitly_wait(30)
        browser.get(response.url)

        self.scroll(browser, 3)

        scrapy_selector = Selector(text=browser.page_source)
        products = scrapy_selector.css('.hm-product-item')
        for idx, product in enumerate(products):
            item = ProductItem()
            item['title'] = product.css('.item-heading > a::text').get()
            item['price'] = product.css('span.price.regular::text').get()
            item['sale_price'] = product.css('span.price.sale::text').get()
            image_url = product.css('img::attr(src)').get()
            if image_url:
                if 'https:' not in image_url:
                    image_url = 'https:' + image_url
                item['image_urls'] = [image_url, image_url]
            else:
                continue
            item['product_link'] = self.base_url + product.css('a::attr(href)').get()
            yield item
        browser.close()
