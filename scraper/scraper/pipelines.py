# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.utils.project import get_project_settings
from itemadapter import ItemAdapter
from elasticsearch import Elasticsearch


class ScraperPipeline:
    def process_item(self, item, spider):
        return item


class ElasticsearchPipeline:
    """
    ElasticsearchPipeline is responsible for writing scraping results
    into elastic cluster.
    """

    def __init__(self):
        self.id_ptr = 1
        self.settings = get_project_settings()
        self.es_cli = Elasticsearch(
            hosts=[
                {
                    "host": self.settings["ELASTICSEARCH_HOST"],
                    "port": self.settings["ELASTICSEARCH_PORT"],
                }
            ]
        )

    def process_item(self, item, spider):
        index_name = self.settings["ELASTICSEARCH_INDEX"]
        result = self.es_cli.index(
            index=index_name, doc_type="post", id=self.id_ptr, body=dict(item)
        )
        self.id_ptr += 1
        print(result)
        return item
