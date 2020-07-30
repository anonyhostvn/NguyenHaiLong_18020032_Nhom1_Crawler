# -*- coding: utf-8 -*-
import scrapy
import json

#HOT 15
#new 30

class BaomoiSpider(scrapy.Spider):
    name = 'baomoi'
    # allowed_domains = ['https://baomoi.com']
    start_urls = ['https://baomoi.com/tin-moi.epi']
    dataCrawled = []
    recentPage = 1
    maxPage = 30

    def extractStoryHeading(self, div):
        for element in div:
            return [element.css('a').attrib['href'], element.css('a::text').get()]
        return ['', '']

    def extractThumbnail(self, div):
        for element in div:
            res = [e.attrib['src'] for e in element.css('img')]
            if len(res) == 1:
                return res[0]
        return ''

    def extractMeta(self, div):
        for elementDiv in div:
            res = [e.attrib['href'] for e in elementDiv.css('.source')] \
                  + [e.attrib['datetime'] for e in elementDiv.css('time')]
            if len(res) == 2:
                return res
        return ['', '']

    def getNextPageUrl(self, div):
        for elementDiv in div:
            listBtn = elementDiv.css('.btn')
            if len(listBtn) == 0:
                return None
            else:
                return listBtn[-1:].attrib['href']
        return None

    def parse(self, response):

        for singleA in response.css('.story'):
            [href, content] = self.extractStoryHeading(singleA.css('.story__heading'))
            [source, time] = self.extractMeta(singleA.css('.story__meta'))
            thumb = self.extractThumbnail(singleA.css('.story__thumb'))

            self.dataCrawled.append({
                'href': response.urljoin(href),
                'content': content,
                'source': response.urljoin(source),
                'time': time,
                'thumb': thumb
            })

        nextPage = self.getNextPageUrl(response.css('.pagination'))
        if nextPage is not None:
            self.recentPage += 1
            if self.recentPage <= self.maxPage:
                yield scrapy.Request(response.urljoin(nextPage), callback=self.parse)

        if self.recentPage == self.maxPage:
            f = open("tiki/spiders/output.json", "w+", encoding="utf-8")
            f.writelines(json.dumps({
                "total": len(self.dataCrawled),
                "data": self.dataCrawled
            }))
            f.close()

        pass
