# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class candidateItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    href = scrapy.Field()

class q_and_a_Item(scrapy.Item):
    question = scrapy.Field()
    description = scrapy.Field()
    answer = scrapy.Field()