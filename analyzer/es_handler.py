from elasticsearch import Elasticsearch


class ElasticsearchHandler:
    """
    ElasticsearchHandler is responsible for all interaction with
    elasticsearch cluster.
    """

    def __init__(self):
        self.id_ptr = 0
        self.es_cli = Elasticsearch(
            hosts=[
                {
                    "host": "localhost",
                    "port": 9200,
                }
            ]
        )


elasticsearch_handler = ElasticsearchHandler()
