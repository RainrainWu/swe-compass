import json

from analyzer.es_handler import elasticsearch_handler


class Analyzer:

    def __init__(self):
        self.es = elasticsearch_handler

    def get_percents(self, terms):

        hold = {}
        amount = int(self.es.es_cli.cat.count(
            index="job_description",
            params={"format": "json"}
        )[0]["count"])
        for term in terms:
            query = {
                "query": {
                    "match": {
                        "description": f"{term}"
                    }
                },
                "size": 0
            }
            result = self.es.es_cli.search(
                index="job_description",
                body=query
            )
            percent = result["hits"]["total"]["value"] / amount
            hold[term] = round(percent * 100, 2)

        return hold
