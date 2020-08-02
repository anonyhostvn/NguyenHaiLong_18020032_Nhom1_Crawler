# -*- coding: utf-8 -*-
import scrapy
import json
import re
from .model.news import News, DomainType

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
    allowed_domains = ['baomoi.com', 'zingnews.vn', 'suckhoedoisong.vn']
    start_urls = ['https://baomoi.com']
    data_crawled = []
    news_data = []
    size = 0
    recent_page = 1
    max_page = 100
    limit_size = 100
    find_command_redirect_regex = "window.location.replace\\(\"[http, https][\\w,\\W]+.[html, htm]\"\\);"

    def add_data_to_pool(self, new_post):

        if not bool(re.match("[\\W,\\w]+/r/[\\W,\\w]+", new_post['href'])):
            return

        for oldPost in self.data_crawled:
            if oldPost['href'] == new_post['href']:
                return

        self.size += 1
        self.data_crawled.append(new_post)

    def zingnews_crawler(self, response):
        data_object = News(response, DomainType.ZINGVN)
        self.news_data.append(data_object.data)

    def suckhoedoisong_crawler(self, response):
        data_object = News(response, DomainType.SUCKHOEDOISONG)
        self.news_data.append(data_object.data)

    def redirect_link(self, response):
        for script_tag in response.css('script'):
            for element in re.findall(self.find_command_redirect_regex, script_tag.get()):
                for link in re.findall("\"[http, https][\\w,\\W]+.[html, htm]\"", element):

                    link_extracted = link[1:-1]
                    domain = re.findall("(\\w+).[com,vn]", link_extracted)[0]

                    print(link_extracted)
                    print(domain)

                    if domain == 'zingnews':
                        yield scrapy.Request(link_extracted, callback=self.zingnews_crawler)
                    elif domain == 'suckhoedoisong':
                        yield scrapy.Request(link_extracted, callback=self.suckhoedoisong_crawler)

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

            for item in self.data_crawled:
                yield scrapy.Request(item['href'], callback=self.redirect_link)
            self.data_crawled.clear()

        pass
