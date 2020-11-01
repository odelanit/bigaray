import time

import scrapy
import urllib.parse
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Stories_1_1'  # name_gender_type
    allowed_domains = ['www.stories.com']
    start_urls = [
        'https://www.stories.com/en/clothing/whats-new.html',
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

        # try:
        #     browser.find_element_by_css_selector('.js-close-button').click()
        #     time.sleep(3)
        # except NoSuchElementException:
        #     print('No close button')

        self.scroll(browser, 3)

        scrapy_selector = Selector(text=browser.page_source)

        products = scrapy_selector.css('div.producttile-wrapper')
        for idx, product in enumerate(products):
            item = ProductItem()
            item['title'] = product.css('.product-title > p::text').get().strip()
            item['price'] = product.css('.m-product-price > span::text').get().strip()
            image_url = product.css('img::attr(src)').get()
            decoded_url = urllib.parse.unquote(image_url)
            if decoded_url:
                if 'https:' not in decoded_url:
                    decoded_url = 'https:' + decoded_url
                hq_image_url = decoded_url.replace('set=key[resolve.width],value[250]', 'set=key[resolve.width],value[500]')
                item['image_urls'] = [decoded_url, hq_image_url]
            else:
                continue
            item['product_link'] = product.css('a.a-link::attr(href)').get()
            yield item
        browser.close()

