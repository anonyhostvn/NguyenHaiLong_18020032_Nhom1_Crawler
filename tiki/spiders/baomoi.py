# -*- coding: utf-8 -*-
import scrapy
import json
import re

# HOT 15
# new 30


def extractStoryHeading(div):
    for element in div:
        return [element.css('a').attrib['href'], element.css('a::text').get()]
    return ['', '']


def extractThumbnail(div):
    for element in div:
        res = [e.attrib['src'] for e in element.css('img')]
        if len(res) == 1:
            return res[0]
    return ''


def extractMeta(div):
    for elementDiv in div:
        res = [e.attrib['href'] for e in elementDiv.css('.source')] \
              + [e.attrib['datetime'] for e in elementDiv.css('time')]
        if len(res) == 2:
            return res
    return ['', '']


class BaomoiSpider(scrapy.Spider):
    name = 'baomoi'
    allowed_domains = ['baomoi.com']
    start_urls = ['https://baomoi.com']
    data_crawled = []
    size = 0
    recent_page = 1
    max_page = 100
    limit_size = 5000

    def add_data_to_pool(self, new_post):

        if not bool(re.match("[\\W,\\w]+/r/[\\W,\\w]+", new_post['href'])):
            return

        for oldPost in self.data_crawled:
            if oldPost['href'] == new_post['href']:
                return

        self.size += 1
        self.data_crawled.append(new_post)

    def parse(self, response):

        if self.size >= self.limit_size:
            return

        for singleA in response.css('.story'):
            if self.size < self.limit_size:
                [href, content] = extractStoryHeading(singleA.css('.story__heading'))
                [source, time] = extractMeta(singleA.css('.story__meta'))
                thumb = extractThumbnail(singleA.css('.story__thumb'))

                self.add_data_to_pool({
                    'href': response.urljoin(href),
                    'content': content,
                    'source': response.urljoin(source),
                    'time': time,
                    'thumb': thumb
                })
            else:
                break

        print(self.size)

        for a_div in response.css('a'):
            if self.size < self.limit_size:
                next_page = a_div.attrib['href']
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
            else:
                break

        if len(self.data_crawled) >= self.limit_size:
            f = open("tiki/spiders/output.json", "w+", encoding="utf-8")
            f.writelines(json.dumps({
                "total": len(self.data_crawled),
                "data": self.data_crawled
            }))
            f.close()

        pass
