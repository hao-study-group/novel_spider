# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.utils.project import get_project_settings
import datetime


class NovelPipeline(object):
    def open_spider(self, spider):
        settings = get_project_settings()
        config = {
            'host': settings.get('MYSQL_HOST'),
            'port': settings.get("MYSQL_PORT"),
            'database': settings.get("MYSQL_DATABASE"),
            'user': settings.get('MYSQL_USER'),
            'password': settings.get('MYSQL_PASSWORD'),
            'charset': settings.get('MYSQL_CHARSET')
        }
        self.conn = pymysql.connect(**config)

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()
        # 查询频道id
        channel_id = 'select id from Channel where channel_name=%s'
        # 查询种类的id
        classfly_id = 'select id from TagModel where tag_name=%s'
        # 查看小说id
        novel_id = 'select id from NovelModel where novel_name=%s'
        # 获取章节是否存在
        chapter_id = 'select id from NovelChaPter where novelchapter_num=%s and novelchapter_cover_id=%s '
        # 添加频道
        add_channel = 'insert into Channel (channel_name) values (%s)'
        # 添加种类
        add_classfly = 'insert into TagModel (tag_name,tag_id_id) values (%s,%s)'
        # 添加小说
        add_novel = 'insert into NovelModel (novel_name,novel_image,novel_user,novel_text,novel_tag_id,novel_time) values (%s,%s,%s,%s,%s,%s)'
        # 添加章节
        add_novel_chapter = 'insert into NovelChaPter (novelchapter_name,novelchapter_text,novelchapter_num,novelchapter_cover_id,novelchapter_time) values (%s,%s,%s,%s,%s)'

        # 添加频道
        try:
            chann_id = self.cursor.execute(channel_id, '男频')
            if not chann_id:
                self.cursor.execute(add_channel, ('男频'))
                chann_id = self.cursor.execute(channel_id, '男频')
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
        # 添加分类
        try:
            xx = self.cursor.execute(classfly_id, item['novel_classfly'])
            if xx:
                class_id = self.cursor.fetchone()[0]
            else:
                self.cursor.execute(add_classfly, (item['novel_classfly'], chann_id))
                self.cursor.execute(classfly_id, item['novel_classfly'])
                class_id = self.cursor.fetchone()[0]
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()

        # # 添加小说
        # try:
        xx = self.cursor.execute(novel_id, item['novel_name'])
        if xx:
            novelid = self.cursor.fetchone()[0]
        else:
            self.cursor.execute(add_novel,
                                (
                                item['novel_name'], item['novel_img'], item['novel_author'], item['novel_synopsis'],
                                class_id, datetime.datetime.now()))
            self.cursor.execute(novel_id, item['novel_name'])
            novelid = self.cursor.fetchone()[0]
            self.conn.commit()
        # except Exception as e:
        #     self.conn.rollback()

        # # 添加章节
        try:
            xx = self.cursor.execute(chapter_id, (item['chapter_id'], novelid))
            if xx:
                chapterid =  self.cursor.fetchone()[0]

            else:
                self.cursor.execute(add_novel_chapter,
                                    (item['chapter_name'], item['chapter_content'], item['chapter_id'], novelid,
                                     datetime.datetime.now()))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()

        return None

    def close_spider(self, spider):
        self.conn.close()




if __name__ == '__main__':
    settings = get_project_settings()
    config = {
        'host': settings.get('MYSQL_HOST'),
        'port': settings.get("MYSQL_PORT"),
        'database': settings.get("MYSQL_DATABASE"),
        'user': settings.get('MYSQL_USER'),
        'password': settings.get('MYSQL_PASSWORD'),
        'charset': settings.get('MYSQL_CHARSET')
    }
    conn = pymysql.connect(**config)
    cu = conn.cursor()
    xx = cu.execute('SELECT  id FROM NovelChaPter   WHERE novelchapter_num=%s',(500000,))
    if xx:
        cu.fetchone()[0]
    else:
        cu.fetchone()
