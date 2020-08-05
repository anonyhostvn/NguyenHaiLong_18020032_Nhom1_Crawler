# Bài tập thu thập dữ liệu với scrapy

## Nhóm 1 - Bài tập tuần 2

* ### Phần 1: Thu thập dữ các bài báo từ trang báo mới
    1. **Spider**
        - Project dùng 2 spider để crawl dữ liệu
            + Spider thứ 1 : `baomoi.py` (spidername: baomoi). Được sử dụng để crawl dữ liệu từ link `www..../${id}.epi`. Dữ liệu chính là đoạn mã có chứa code ``javascript`` redirect sang trang báo nguồn. *Sau khi crawl dữ liệu, chương trình sẽ lưu dữ liệu dưới dạng json trong file `output.json`* 
            + Spider thứ 2 : `newscrawler.py` (spidername: newscrawler). Được sử dụng để đọc file `output.json` được crawl ở spider `baomoi`. Sau đó bóc tách *url* trang báo nguồn từ đoạn code `javascript` rồi request `GET` vào *url* đó. Hàm `parse()` sẽ bóc tách nội dung của bài báo từ `response` trả về sau đó lưu vào file `news_DB.json`
    2. **Định dạng dữ liệu**
        - File `output.json`:
             ```json
          { 
                "total": number, // tổng số dữ liệu crawl được
                "data": [ 
                  { 
                    "href": string, // link tới trang .epi của baomoi,
                    "content": string, // nội dung tóm tắt của bài báo
                    "thumb": string, // link ảnh của bài báo
                    "source": string // Link dẫn tới Category của bài báo         
                  }
               ]
          }
          ```
         - File `newscrawler.py`:
             ```json
           { 
             "title": string, // tiêu đề của bài báo
             "author": string, // tác giả của bài báo
             "time_publish": string, // thời gian xuất bản của bài báo
             "summary": string, // tóm tắt bài báo 
             "body": string, // nội dung chính của bài báo
             "tag": [string] // tập các tag của bài báo   
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

* ### Phần 2: Thu thập dữ liệu sản phẩm từ trang