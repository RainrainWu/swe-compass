# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from es_handler import elasticsearch_handler


class ScraperPipeline:
    def process_item(self, item, spider):
        return item


class ElasticsearchPipeline:
    """
    ElasticsearchPipeline is responsible for writing scraping results
    into elastic cluster.
    """

    def __init__(self):
        self.es_handler = elasticsearch_handler

    def process_item(self, item, spider):
        self.es_handler.write_index(dict(item))
        return item
