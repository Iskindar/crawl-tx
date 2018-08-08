# -*- coding: utf-8 -*-
import scrapy
from CrawlMeiziTu.items import CrawlmeizituItem
#from CrawlMeiziTu.items import CrawlmeizituItemPage
import time
class MeizituSpider(scrapy.Spider):
    name = "Meizitu"
    #allowed_domains = ["meizitu.com/"]

    start_urls = []
    last_url = []
    with open('..//url.txt', 'r') as fp:
        crawl_urls = fp.readlines()
        for start_url in crawl_urls:
            last_url.append(start_url.strip('\n'))
    start_urls.append("".join(last_url[-1]))


    def parse(self, response):
        selector = scrapy.Selector(response)
        #item = CrawlmeizituItemPage()

        next_pages = selector.xpath("//*[@class='n']/@href").extract()
        next_pages_text = selector.xpath("//*[@class='n']/text()").extract()
        all_urls = []
        print(next_pages)
        if '下一页' in next_pages_text:
            next_url = "http://moe.005.tv/tx/{}".format(next_pages[0])
            with open('..//url.txt', 'a+') as fp:
                fp.write('\n')
                fp.write(next_url)
                fp.write("\n")
            request = scrapy.http.Request(next_url, callback=self.parse)
            time.sleep(2)
            yield request

        all_info = selector.xpath("//*[@class='zhuti_w_list']/ul/li/a")
        #读取每个图片夹的连接
        for info in all_info:
            links = info.xpath("//*[@class='zhuti_w_list']/ul/li/a/@href").extract()
        for link in links:
            request = scrapy.http.Request(link, callback=self.parse_item)
            time.sleep(1)
            yield request

    #抓取每个文件夹的信息
    def parse_item(self, response):
        item = CrawlmeizituItem()
        selector = scrapy.Selector(response)

        image_title = selector.xpath("//div[@class='content_w_box']/h1/text()").extract()
        image_url = selector.xpath("//*[@class='zhuti_w_list']/ul/li/a/@href").extract()

        if selector.xpath("//div[@class='content_nr']/div/img/@src").extract():
            image_src = selector.xpath("//div[@class='content_nr']/div/img/@src").extract()
        else:
            image_src = selector.xpath("//div[@class='content_nr']//img/@src").extract()
        if selector.xpath("//div[@class='content_nr']/div").extract():
             pic_name =''.join(selector.xpath("//div[@class='content_nr']/div/text()").extract()).split()
        else:
             pic_name = selector.xpath("//div[@class='content_nr']/div").extract()
         #//*[@id="maincontent"]/div/p/img/@alt
        item['title'] = image_title
        item['url'] = image_url

        item['src'] = image_src
        item['alt'] = pic_name[0:len(image_src)]
        print(item)
        time.sleep(1)
        yield item
