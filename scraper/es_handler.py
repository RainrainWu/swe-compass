from elasticsearch import Elasticsearch
from scrapy.utils.project import get_project_settings


class ElasticsearchHandler:
    """
    ElasticsearchHandler is responsible for all interaction with
    elasticsearch cluster.
    """

    def __init__(self):
        self.id_ptr = 0
        self.settings = get_project_settings()
        self.es_cli = Elasticsearch(
            hosts=[
                {
                    "host": self.settings["ELASTICSEARCH_HOST"],
                    "port": self.settings["ELASTICSEARCH_PORT"],
                }
            ]
        )

    def write_index(self, item):
        """
        write_index will write the content of specified index in
        elasticsearch cluster.
        """
        index_name = self.settings["ELASTICSEARCH_INDEX"]
        result = self.es_cli.index(index=index_name, id=self.id_ptr, body=item)
        self.id_ptr += 1


elasticsearch_handler = ElasticsearchHandler()
