import time

import scrapy
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Pull-bear_1_1'  # name_gender_type
    allowed_domains = ['www.pullandbear.com']
    start_urls = [
        'https://www.pullandbear.com/us/woman/new-c1030017536.html'
    ]

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
        time.sleep(30)

        self.scroll(browser, 10)

        scrapy_selector = Selector(text=browser.page_source)
        products = scrapy_selector.css('.c-tile--product')
        for product in products:
            item = ProductItem()
            item['title'] = product.css('.name::text').get().strip()
            item['price'] = product.css('.product-price--price::text').get().strip()
            image_url = product.css('img.image-responsive::attr(src)').get()
            if image_url:
                if 'https:' not in image_url:
                    image_url = 'https:' + image_url
                item['image_urls'] = [image_url, image_url]
            else:
                continue
            item['product_link'] = product.css('a::attr(href)').get()
            yield item
        browser.close()
