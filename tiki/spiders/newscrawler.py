import scrapy
import json
import re
from .model.news import News, DomainType


class NewsCrawlerSpider(scrapy.Spider):
    name = 'newscrawler'
    allowed_domains = [
        'baomoi.com',
        'zingnews.vn',
        'suckhoedoisong.vn',
        'nguoiduatin.vn',
        'vietnamnet.vn',
        'nld.com.vn',
        'plo.vn',
        'baotintuc.vn',
        'baoquocte.vn',
        'baogiaothong.vn',
        'saostar.vn',
        'kienthuc.net.vn'
    ]
    news_data = []
    find_command_redirect_regex = "window.location.replace\\(\"[http, https][\\w,\\W]+.[html, htm]\"\\);"

    def start_requests(self):
        f = open("tiki/spiders/output.json")
        data = json.load(f)
        for record in data['data']:
            yield scrapy.Request(record['href'], callback=self.parse)
        f.close()

    def zingnews_crawler(self, response):
        data_object = News(response, DomainType.ZINGVN)
        self.news_data.append(data_object.data)

    def suckhoedoisong_crawler(self, response):
        data_object = News(response, DomainType.SUCKHOEDOISONG)
        self.news_data.append(data_object.data)

    def nguoiduatin_crawler(self, response):
        data_object = News(response, DomainType.NGUOIDUATIN)
        self.news_data.append(data_object.data)

    def vietnamnet_crawler(self, response):
        data_object = News(response, DomainType.VIETNAMNET)
        self.news_data.append(data_object.data)

    def nld_crawler(self, response):
        data_object = News(response, DomainType.NLD)
        self.news_data.append(data_object.data)

    def plo_crawler(self, response):
        data_object = News(response, DomainType.PLO)
        self.news_data.append(data_object.data)

    def baotintuc_crawler(self, response):
        data_object = News(response, DomainType.BAOTINTUC)
        self.news_data.append(data_object.data)

    def baoquocte_crawler(self, response):
        data_object = News(response, DomainType.BAOQUOCTE)
        self.news_data.append(data_object.data)

    def baogiaothong_crawler(self, response):
        data_object = News(response, DomainType.BAOGIAOTHONG)
        self.news_data.append(data_object.data)

    def saostar_crawler(self, response):
        data_object = News(response, DomainType.SAOSTAR)
        self.news_data.append(data_object.data)

    def kienthuc_crawler(self, response):
        data_object = News(response, DomainType.KIENTHUC)
        self.news_data.append(data_object.data)

    def parse(self, response):
        if len(self.news_data) >= 14000:
            return

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
                    elif domain == 'nguoiduatin':
                        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
                        yield scrapy.Request(link_extracted, callback=self.nguoiduatin_crawler, headers=headers)
                    elif domain == 'vietnamnet':
                        yield scrapy.Request(link_extracted, callback=self.vietnamnet_crawler)
                    elif domain == 'nld':
                        yield scrapy.Request(link_extracted, callback=self.nld_crawler)
                    elif domain == 'plo':
                        yield scrapy.Request(link_extracted, callback=self.plo_crawler)
                    elif domain == 'baotintuc':
                        yield scrapy.Request(link_extracted, callback=self.baotintuc_crawler)
                    elif domain == 'baoquocte':
                        yield scrapy.Request(link_extracted, callback=self.baoquocte_crawler)
                    elif domain == 'baogiaothong':
                        yield scrapy.Request(link_extracted, callback=self.baogiaothong_crawler)
                    elif domain == 'saostar':
                        yield scrapy.Request(link_extracted, callback=self.saostar_crawler)
                    elif domain == 'kienthuc':
                        yield scrapy.Request(link_extracted, callback=self.kienthuc_crawler)

                    if len(self.news_data) >= 14000:
                        f = open("tiki/spiders/news_DB.json", "w+", encoding='utf-8')
                        f.write(json.dumps(self.news_data))
                        f.close()

                    print('news data size : ' + str(len(self.news_data)))
