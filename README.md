# Bài tập thu thập dữ liệu với scrapy

## Nguyễn Hải Long - 18020032 - Nhóm 1 - Bài tập tuần 2

* ### Phần 1: Thu thập dữ các bài báo từ trang báo mới
    1. **Spider**
        - Project dùng 2 spider để crawl dữ liệu
            + Spider thứ 1 : `baomoi.py` (spidername: baomoi). Được sử dụng để crawl dữ liệu bao gồm tiêu đề, ảnh, link (có dạng : `www.baomoi.com/.../${id}.epi`). Link này sẽ cho ra respone là đoạn mã `html` có chứa code ``javascript`` redirect sang trang báo nguồn.
                > Ví dụ
                ```html
                <!DOCTYPE html>
                <html xmlns="http://www.w3.org/1999/xhtml">
                
                <head>
                    <title>
                        Thêm 41 ca mắc COVID-19, trong đó 40 ca liên quan đến Đà Nẵng, Việt Nam có 713 bệnh nhân - Báo Sức Khỏe & Đời
                        Sống
                    </title>
                    <meta name="referrer" content="unsafe-url" />
                    <link rel="canonical"
                        href="https://baomoi.com/them-41-ca-mac-covid-19-trong-do-40-ca-lien-quan-den-da-nang-viet-nam-co-713-benh-nhan/c/35934364.epi" />
                    <meta name="description"
                        content="Bản tin 18h ngày 5/8 của Ban Chỉ đạo Quốc gia cho biết đã ghi nhận thêm 41 ca mắc mới COVID-19, trong đó có 34 ca tại Đà Nẵng, 04 ca tại Lạng Sơn, 02 ca tại Bắc Giang, 01 ca nhập cảnh được cách ly ngay. Việt Nam hiện có 713 bệnh nhân" />
                    <meta name="keywords"
                        content="nhập cảnh,cách ly,SARS-COV-2,ca bệnh,Ban chỉ đạo quốc gia,bệnh nhân,IO4405,ca nhiễm,Đà Nẵng,dương tính,Bệnh viện Đà Nẵng,Lạng Sơn,Bắc Giang,Liên Chiều,sân bay Tân Sân Nhất,cộng đồng,Bệnh viện Bà Rịa,dịch,Nhi Đà Nẵng,âm tính" />
                
                    <script async>
                        (function (i, s, o, g, r, a, m) {
                                i['GoogleAnalyticsObject'] = r;
                                i[r] = i[r] || function () {
                                    (i[r].q = i[r].q || []).push(arguments);
                                }, i[r].l = 1 * new Date();
                                a = s.createElement(o),
                                        m = s.getElementsByTagName(o)[0];
                                a.async = 1;
                                a.src = g;
                                m.parentNode.insertBefore(a, m);
                            })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');
                            ga('create', 'UA-309591-61', 'auto');
                            ga('send', 'pageview', {'page': window.location.pathname + window.location.search + window.location.hash});
                    </script>
                </head>
                
                <body onpageshow="load()" onload="load()">
                    <input type="hidden" class="bm-track" data-key="web_all" data-value="" />
                    <input type="hidden" class="bm-track" data-key="web_article" data-value="35934364" />
                    <input type="hidden" class="bm-track" data-key="web_article_redirect" data-value="35934364" />
                    <script src="//baomoi-static.zadn.vn/web/js/tracking-dist.js?v=1.2.0"></script>
                
                    <script type="text/javascript">
                        var isRedirected = false;
                        function redirect() {
                            if (!isRedirected) {
                                isRedirected = true;
                                var userAgent = navigator.userAgent.toLowerCase();
                                var isBot = /bot|googlebot|crawler|spider|robot|crawling/i.test(userAgent);
                
                                if (!isBot)
                                    window.location.replace("https://suckhoedoisong.vn/them-41-ca-mac-covid-19-trong-do-40-ca-lien-quan-den-da-nang-viet-nam-co-713-benh-nhan-n178251.html");
                                else
                                    window.location.replace("/them-41-ca-mac-covid-19-trong-do-40-ca-lien-quan-den-da-nang-viet-nam-co-713-benh-nhan/c/35934364.epi");
                            }
                        }
                        function load() {
                            setTimeout(redirect, 100);
                        }
                    </script>
                
                </body>
                
                </html>
                ```                                                                                                                                                                                                                                                  
                *Sau khi crawl dữ liệu, chương trình sẽ lưu dữ liệu dưới dạng json trong file `output.json`* 
            + Spider thứ 2 : `newscrawler.py` (spidername: newscrawler). Được sử dụng để đọc file `output.json` được crawl ở spider `baomoi`. Sau đó bóc tách *url* trang báo nguồn từ đoạn code `javascript` rồi request `GET` vào *url* đó. Hàm `parse()` sẽ bóc tách nội dung của bài báo từ `response` trả về sau đó lưu vào file `news_DB.json`

    2. **Định dạng dữ liệu**
        - File `output.json`:
             ```json
          { 
                "total": "number", // tổng số dữ liệu crawl được
                "data": [ 
                  { 
                    "href": "string", // link tới trang .epi của baomoi,
                    "content": "string", // nội dung tóm tắt của bài báo
                    "thumb": "string", // link ảnh của bài báo
                    "source": "string" // Link dẫn tới Category của bài báo         
                  }
               ]
          }
          ```
         - File `newscrawler.json`:
             ```json
           { 
             "title": "string", // tiêu đề của bài báo
             "author": "string", // tác giả của bài báo
             "time_publish": "string", // thời gian xuất bản của bài báo
             "summary": "string", // tóm tắt bài báo 
             "body": "string", // nội dung chính của bài báo
             "tag": ["string"] // tập các tag của bài báo   
           }
           ```
    3. Một số file phụ khác
        - `model/domaintype.py` Một enum type lưu các biến tương ứng cho mỗi `source` mà chương trình crawl.
        - `model/news.py` Một class tương ứng với toàn thể nội dung mỗi bài báo (bao gồm title, author, ... ). Trong đó có cả các đoạn code để crawl dữ liệu tương ứng với từng source.
    4. Thứ tự chạy
        * Step 1: chạy dòng lệnh 
            ~~~
                scrapy crawl baomoi
            ~~~
        * Step 2: chạy dòng lệnh 
            ~~~
                scrapy crawl newscrawler
            ~~~   
    5. Giải thích qua về mã nguồn
        * File `baomoi.py`:
            - Một số biến quan trọng:
                + `data_crawled = []`: Mảng lưu các record crawl được.
                + `url_pool = set({})`: Tập các url đã request rồi. Lưu với mục đích tránh trùng lặp
                + `queue_url = []`: Ta sẽ lưu các url vào queue và request dần dần. Queue chỉ được có tối đa 100 phần tử (được config tại biến limit_queue) để tránh request thừa.
                +  `limit_size = 50000`: Giới hạn số record mà ta sẽ crawl từ baomoi
            - Một số hàm quan trọng:
                + `add_data_to_pool()`: Thêm dữ liệu vào biến `data_crawled`. Bao gồm cả công việc check xem url đó có đúng là url dẫn đến bài báo hay không vào check trùng lặp với các url có trong pool .
                + `parse()`:
                    + Lấy các mục báo từ web rồi bóc tách dữ liệu thêm url vào *queue* và *pool* 
                    ```python
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
                    ```    
                    + Lấy url từ queue và request
                    ```python
                     while self.size < self.limit_size and len(self.queue_url) > 0:
                            url = self.queue_url[0]
                            self.queue_url.pop(0)
                            yield scrapy.Request(response.urljoin(url), callback=self.parse)
                    ```
                    + Nếu đã đủ số lượng record cần lấy thì ghi vào file
                    ```python
                      if len(self.data_crawled) >= self.limit_size:
                    
                                f = open("tiki/spiders/output.json", "w+", encoding="utf-8")
                                f.writelines(json.dumps({
                                    "total": len(self.data_crawled),
                                    "data": self.data_crawled
                                }))
                                f.close()
                    ```
        * File `newscrawler.py`
            + Một số biến quan trọng:
                -  `news_data = []`: List các bài báo đã được crawl.
            + Một số hàm quan trọng:
                - `parse()`: Bóc tách source type và sử dụng module crawl dữ liệu phù hợp với từng source

* ### Phần 2: Thu thập dữ liệu sản phẩm từ trang websosanh
    1. **Spider**:
        - Chỉ có duy nhất 1 spider. Do cấu trúc link của websosanh đơn giản nên ta có thể for từng id của sản phẩm để get dữ liệu. 
    2. **Định dạng dữ liệu**
        - File `product.json`:
            ```json
                "title": "string", // tiêu đề của sản phẩm
                "brand": "string", // Thương hiệu của sản phẩm
                "desc": "string", // mô tả ngắn sản phẩm
                "price": "number", // giá 
                "full_desc": "string" // Mô tả đầy đủ sản phẩm định dạng HTML       
            ```
          
### Link dẫn tới thư mục chứa data sau khi crawl:
> <a href="https://drive.google.com/drive/folders/1SfYuXOzDiQdMOMHVb_cJgr6QmVMVOgSa?usp=sharing" target="_blank"> Data_Crawled </a> 
