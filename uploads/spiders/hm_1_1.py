import time

import scrapy
from django.utils import timezone
from parsel import Selector
from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from scraping.models import Scraper
from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Hm_1_1'  # name_gender_type
    allowed_domains = ['www2.hm.com']
    start_urls = [
        'https://www2.hm.com/en_ca/women/New-arrivals/clothes.html'
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

    def parse(self, response, **kwargs):
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options)
        # browser = webdriver.Firefox()
        browser.implicitly_wait(30)
        browser.get(response.url)
        try:
            elements = browser.find_elements_by_css_selector('.slick-dots > li')
            for el in elements:
                el.click()
                time.sleep(10)
        except NoSuchElementException:
            print('No slick dots button')

        scrapy_selector = Selector(text=browser.page_source)
        products = scrapy_selector.css('.hm-product-item')
        for idx, product in enumerate(products):
            item = ProductItem()
            item['title'] = product.css('.item-heading > a::text').get()
            price = product.css('span.price::text').get().strip()
            item['price'] = price
            image_url = product.css('img::attr(src)').get()
            if image_url:
                item['image_urls'] = [image_url, image_url]
            else:
                continue
            item['product_link'] = self.base_url + product.css('a::attr(href)').get()
            yield item
        browser.close()
