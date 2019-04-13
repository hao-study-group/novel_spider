# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    """
    novel_name: 小说名称
    novel_author：小说作者
    novel_synopsis: 小说简介
    chapter_id : 章节id
    chapter_name：章节名称
    chapter_content：章节内容
    novel_img : 小说封面
    novel_classfly : 小说分类

    """
    novel_name = scrapy.Field()
    novel_author = scrapy.Field()
    novel_synopsis = scrapy.Field()
    chapter_id = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_content = scrapy.Field()
    novel_img = scrapy.Field()
    novel_classfly = scrapy.Field()







