# -*- coding: utf-8 -*-
import scrapy
from novel import items
from novel.db import DB_REDIS


class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    # allowed_domains = ['www.biquge.com']
    start_urls = ['http://www.xbiquge.la/xiaoshuodaquan/']

    def parse(self, response):
        self.conn = DB_REDIS()
        '''
        解析全部小说
        :param response:
        :return:
        '''
        type_list = response.xpath('//*[@id="main"]/div[@class="novellist"]')
        z = 1
        for i in type_list:
            novel_list = i.xpath('./ul/li/a/@href').getall()
            for novel_url in novel_list:
                if z == 1:
                    continue
                yield scrapy.Request(url=novel_url, callback=self.novel_chapter_list)
                break
            z += 1
            if z > 3:
                break

    def novel_chapter_list(self, response):
        novel_name = response.xpath('//*[@id="info"]/h1[1]/text()').get()
        novel_author = response.xpath('//*[@id="info"]/p[1]/text()').get()
        novel_synopsis = response.xpath('//*[@id="intro"]/p[2]/text()').get()
        novel_img = response.xpath('//*[@id="fmimg"]/img/@src').get()
        novel_classfly = response.xpath(
            '//*[@id="wrapper"]/div[@class="box_con"]/div[@class="con_top"]/a[2]/text()').get()
        chapter_list = response.xpath('//*[@id="list"]/dl/dd')

        for index, i in enumerate(chapter_list, 1):
            chapter_name = i.xpath('./a/text()').get()
            chapter_url = 'http://www.xbiquge.la/' + i.xpath('./a/@href').get()
            dic = {}
            dic['novel_name'] = novel_name
            print('爬取小说：',novel_name)
            dic['novel_author'] = novel_author
            dic['novel_synopsis'] = novel_synopsis
            dic['chapter_name'] = chapter_name
            dic['chapter_id'] = index
            dic['novel_img'] = novel_img
            dic['novel_classfly'] = novel_classfly
            xx = self.conn.insert(chapter_url)
            # if xx:
            yield scrapy.Request(url=chapter_url, callback=self.chapter_content, meta={'dic': dic})
            # else:
            #     print('这个页面已经爬取过')

    def chapter_content(self, response):
        item = items.NovelItem()
        for k, v in response.meta['dic'].items():
            item[k] = v
        chapter_content = response.xpath('//*[@id="content"]//text()').getall()
        chapter_content = ''.join(chapter_content[0:-2])
        item['chapter_content'] = chapter_content
        yield item
