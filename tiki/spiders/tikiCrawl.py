# -*- coding: utf-8 -*-
import scrapy


class TikicrawlSpider(scrapy.Spider):
    name = 'tikiCrawl'
    allowed_domains = ['https://tiki.vn']
    start_urls = ['https://tiki.vn']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        f = open('tiki/spiders/output.html', 'w+')
        f.write(response.css('p').get(1))
        f.write('------------------  \n')
        f.close()
        pass
