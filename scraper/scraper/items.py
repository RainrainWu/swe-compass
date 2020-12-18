# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nameOfAuthor = scrapy.Field()
    linkOfAuthorProfile = scrapy.Field()
    article = scrapy.Field()
    articleLink = scrapy.Field()
    postingTime = scrapy.Field()
    recommendation = scrapy.Field()