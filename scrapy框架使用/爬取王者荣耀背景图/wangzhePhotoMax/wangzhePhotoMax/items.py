# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WangzhephotomaxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    hero_name = scrapy.Field()
    skin_url = scrapy.Field()
    skin_name = scrapy.Field()

