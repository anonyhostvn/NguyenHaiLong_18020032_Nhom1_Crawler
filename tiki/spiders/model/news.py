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

    def nguoiduatin_crawler(self, response):
        for header_tag in response.css('header'):
            for title in header_tag.css('.title::text'):
                self.data['title'] = title.get()

        for datetime_class in response.css('.datetime'):
            for time_publish in datetime_class.css('p::text'):
                self.data['time_publish'] = time_publish.get()

        for article in response.css('article'):
            self.data['body'] = article.get()
            for p_tag in article.css('p'):
                for strong_tag in p_tag.css('strong::text'):
                    self.data['author'] = strong_tag.get()

        for list_tag in response.css('.tags'):
            for li_tag in list_tag.css('li'):
                for a_tag in li_tag.css('a::text'):
                    self.data['tag'].append(a_tag.get())

    def vietnamnet_crawler(self, response):
        for title in response.css('.title::text'):
            self.data['title'] = title.get()
        for time_publish in response.css('.ArticleDate::text'):
            self.data['time_publish'] = time_publish.get()
        for body in response.css('.ArticleContent'):
            self.data['body'] = body.get()
        for tag_box in response.css('.tagBoxContent'):
            for li_tag in tag_box.css('li'):
                for tag in li_tag.css('a::text'):
                    self.data['tag'].append(tag.get())

    def nld_crawler(self, response):
        for title in response.css('.title-content::text'):
            self.data['title'] = title.get()
        for time_publish in response.css('.pdate::text'):
            self.data['time_publish'] = time_publish.get()
        for summary in response.css('.sapo-detail::text'):
            self.data['summary'] = summary.get()
        for body in response.css('.content-news-detail'):
            self.data['body'] = body.get()
        for author in response.css('.author::text'):
            self.data['author'] = author.get()
        for tag in response.css('.tagname::text'):
            self.data['tag'].append(tag.get())

    def plo_crawler(self, response):
        for title in response.css('.main-title::text'):
            self.data['title'] = title.get()
        for meta in response.css('.meta'):
            for time_publish in meta.css('time::text'):
                self.data['time_publish'] = time_publish.get()
        for summary in response.css('.sapo'):
            self.data['summary'] = summary.get()
        for body in response.css('#main_detail'):
            self.data['body'] = body.get()
        for tag in response.css('.tags a ::text'):
            self.data['tag'].append(tag.get())

    def baotintuc_crawler(self, response):
        for title in response.css('.detail-title ::text'):
            self.data['title'] = title.get()
        for time_publish in response.css('.action-link .date .txt ::text'):
            self.data['time_publish'] = time_publish.get()
        for summary in response.css('.sapo ::text'):
            self.data['summary'] = summary.get()
        for body in response.css('.content_wrapper .contents'):
            self.data['body'] = body.get()
        for author in response.css('.author strong ::text'):
            self.data['author'] = author.get()
        for tag in response.css('#plhMain_NewsDetail1_divTags ul li a strong ::text'):
            self.data['tag'].append(tag.get())

    def baoquocte_crawler(self, response):
        for title in response.css('.titleDetailNews ::text'):
            self.data['title'] = title.get()
        for time_publish in response.css('.inforAuthor .tg .dateUp .format_time ::text'):
            self.data['time_publish'] = time_publish.get()
        for summary in response.css('.viewsDtail .padB10 .f-16 strong ::text'):
            self.data['summary'] = summary.get()
        for body in response.css('.viewsDtail .viewsDtailContent'):
            self.data['body'] = body.get()
        for author in response.css('.inforAuthor .tg .clorOr ::text'):
            self.data['author'] = author.get()
        for tag in response.css('.boxTags .tagsCould li a ::text'):
            self.data['tag'].append(tag.get())

    def baoquocte_crawler(self, response):
        for title in response.css('.titleDetailNews ::text'):
            self.data['title'] = title.get()
        for time_publish in response.css('.inforAuthor .tg .dateUp .format_time ::text'):
            self.data['time_publish'] = time_publish.get()
        for summary in response.css('.viewsDtail .padB10 .f-16 strong ::text'):
            self.data['summary'] = summary.get()
        for body in response.css('.viewsDtail .viewsDtailContent'):
            self.data['body'] = body.get()
        for author in response.css('.inforAuthor .tg .clorOr ::text'):
            self.data['author'] = author.get()
        for tag in response.css('.boxTags .tagsCould li a ::text'):
            self.data['tag'].append(tag.get())

    def baogiaothong_crawler(self, response):
        for title in response.css('.postTit ::text'):
            self.data['title'] = title.get()
        for time_publish in response.css('.dateArt ::text'):
            self.data['time_publish'] = time_publish.get()
        for summary in response.css('.descArt ::text'):
            self.data['summary'] = summary.get()
        for body in response.css('.bodyArt'):
            self.data['body'] = body.get()
        for author in response.css('.author .name ::text'):
            self.data['author'] = author.get()

    def saostar_crawler(self, response):
        for title in response.css('.art-title ::text'):
            self.data['title'] = title.get()
        for time_publish in response.css('.time ::text'):
            self.data['time_publish'] = time_publish.get()
        for summary in response.css('.art-sapo ::text'):
            self.data['summary'] = summary.get()
        for body in response.css('.art-content'):
            self.data['body'] = body.get()
        # for author in response.css('.author .name ::text'):
        #     self.data['author'] = author.get()

    def kienthuc_crawler(self, response):
        for title in response.css('.title  ::text'):
            self.data['title'] = title.get()
        for time_publish in response.css('.cms-date'):
            self.data['time_publish'] = time_publish.attrib['content']
        for summary in response.css('.summary div ::text'):
            self.data['summary'] = summary.get()
        for body in response.css('.topContent'):
            self.data['body'] = body.get()
        for author in response.css('.author::text'):
            self.data['author'] = author.get()

    def __init__(self, response, domain):

        self.data = {
            'title': '',
            'author': '',
            'time_publish': '',
            'summary': '',
            'body': '',
            'tag': []
        }

        if domain == DomainType.ZINGVN:
            self.zingvn_crawl_data(response)
        elif domain == DomainType.SUCKHOEDOISONG:
            self.suckhoedoisong_crawler(response)
        elif domain == DomainType.NGUOIDUATIN:
            self.nguoiduatin_crawler(response)
        elif domain == DomainType.VIETNAMNET:
            self.vietnamnet_crawler(response)
        elif domain == DomainType.NLD:
            self.nld_crawler(response)
        elif domain == DomainType.PLO:
            self.plo_crawler(response)
        elif domain == DomainType.BAOTINTUC:
            self.baotintuc_crawler(response)
        elif domain == DomainType.BAOQUOCTE:
            self.baoquocte_crawler(response)
        elif domain == DomainType.BAOGIAOTHONG:
            self.baogiaothong_crawler(response)
        elif domain == DomainType.SAOSTAR:
            self.saostar_crawler(response)
        elif domain == DomainType.KIENTHUC:
            self.kienthuc_crawler(response)
