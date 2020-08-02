from .domaintype import DomainType


class News:
    data = {
        'title': '',
        'author': '',
        'time_publish': '',
        'summary': '',
        'body': '',
        'tag': []
    }

    def zingvn_crawl_data(self, response):

        for header_section in response.css('.the-article-header'):

            for header_title in header_section.css('.the-article-title::text'):
                self.data['title'] = header_title.get()

            for author in header_section.css('.the-article-author'):
                for author_name in author.css('a::text'):
                    self.data['author'] = author_name.get()

            for time_publish in header_section.css('.the-article-publish::text'):
                self.data['time_publish'] = time_publish.get()

        for main_section in response.css('.main'):
            for summary in main_section.css('.the-article-summary::text'):
                self.data['summary'] = summary.get()

            for body in main_section.css('.the-article-body'):
                self.data['body'] = body.get()

            for list_tag in main_section.css('.the-article-tags'):
                for tag in list_tag.css('*::text'):
                    if tag.get().strip() != '':
                        self.data['tag'].append(tag.get())

    def suckhoedoisong_crawler(self, response):
        for title in response.css('.title-detail::text'):
            self.data['title'] = title.get()
        for author in response.css('.author::text'):
            self.data['author'] = author.get()
        for time_publish in response.css('.post-time::text'):
            self.data['time_publish'] = time_publish.get()
        for summary in response.css('.sapo_detail::text'):
            self.data['summary'] = summary.get()
        for body in response.css('#content_detail_news'):
            self.data['body'] = body.get()
        for tag in response.css('.tag_detail_item::text'):
            self.data['tag'].append(tag.get())

    def __init__(self, response, domain):
        if domain == DomainType.ZINGVN:
            self.zingvn_crawl_data(response)
        elif domain == DomainType.SUCKHOEDOISONG:
            self.suckhoedoisong_crawler(response)
