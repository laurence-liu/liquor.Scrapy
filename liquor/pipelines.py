# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2

class LiquorPipeline(object):
    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres' # your username
        password = '***' # your password
        database = 'dear-liquor'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("INSERT INTO cocktails(name, link, image, introduce, material, steps, basespirit) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                        ,(item['name'], item['link'], item['image'], item['introduce'], item['material'], item['steps'], item['basespirit']))
        self.connection.commit()
        return item