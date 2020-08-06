# -*- coding: utf-8 -*-
import scrapy
import json


class SosanhgiaSpider(scrapy.Spider):
    name = 'sosanhgia'
    allowed_domains = ['sosanhgia.com']
    start_urls = ['https://www.sosanhgia.com/p186117.html']
    start_product = 186117
    product_crawled = []
    limit_number_product = 5000

    def get_url(self, id):
        return 'https://www.sosanhgia.com/p' + str(id) + '.html'

    def start_requests(self):
        for i in range(self.limit_number_product + 5000):
            print(i)
            yield scrapy.Request(self.get_url(self.start_product + i), callback=self.parse)

    def parse(self, response):

        if len(self.product_crawled) > self.limit_number_product:
            return
        elif len(self.product_crawled) == self.limit_number_product:
            f = open('tiki/spiders/product.json', 'w+')
            f.writelines(json.dumps(self.product_crawled))
            f.close()

        for page_not_found in response.css('.page-notfound'):
            print('page not found')
            return

        product = {}

        for title in response.css('.product-info-container a h1 ::text'):
            product['title'] = title.get()

        for brand in response.css('.product-info-container .brand a ::text'):
            product['brand'] = brand.get()

        for desc in response.css('.short-desc p ::text'):
            product['desc'] = desc.get()

        for price in response.css('.store-price::text'):
            product['price'] = price.get()

        for full_desc in response.css('.description-content'):
            product['full_desc'] = full_desc.get()

        self.product_crawled.append(product)

        pass
