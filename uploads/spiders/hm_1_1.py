import os
import time
from shutil import which
from urllib.parse import urlencode

import scrapy
from parsel import Selector
from scrapy.utils.project import get_project_settings
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Hm_1_1'  # name_gender_type
    allowed_domains = ['www2.hm.com']
    start_urls = [
        'https://www2.hm.com/en_ca/women/New-arrivals/clothes.html'
    ]
    base_url = 'https://www2.hm.com'

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
