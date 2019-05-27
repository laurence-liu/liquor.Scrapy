# -*- coding: utf-8 -*-
import scrapy


class LiquorCrawlerSpider(scrapy.Spider):
    name = 'liquor_crawler'
    allowed_domains = ['liquor.com']
    start_urls = ['http://liquor.com/']

    def parse(self, response):
        pass
