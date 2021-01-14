import json

from analyzer.es_handler import elasticsearch_handler


class Executor:
    es = elasticsearch_handler
    doc_count = int(
        es.es_cli.cat.count(index="job_description", params={"format": "json"})[0][
            "count"
        ]
    )

    @classmethod
    def get_union_percent(cls, items):
        query = {
            "query": {
                "bool": {
                    "should": [
                        {"match_phrase": {"description": item}}
                        if " " in item
                        else {"match": {"description": item}}
                        for item in items
                    ],
                    "minimum_should_match": 1,
                }
            }
        }
        result = cls.es.es_cli.search(index="job_description", body=query)
        percent = result["hits"]["total"]["value"] / cls.doc_count
        return round(percent * 100, 2)

    @classmethod
    def get_intersect_percent(cls, items):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match_phrase": {"description": item}}
                        if " " in item
                        else {"match": {"description": item}}
                        for item in items
                    ]
                }
            }
        }
        result = cls.es.es_cli.search(index="job_description", body=query)
        percent = result["hits"]["total"]["value"] / cls.doc_count
        return round(percent * 100, 2)

    @classmethod
    def get_each_percents(cls, phrases):

        hold = {}
        for phrase in phrases:
            query = {
                "query": {
                    "match_phrase" if " " in item else "match": {"description": phrase}
                },
                "size": 0,
            }
            result = cls.es.es_cli.search(index="job_description", body=query)
            percent = result["hits"]["total"]["value"] / cls.doc_count
            hold[phrase] = round(percent * 100, 2)
        return hold

    @classmethod
    def get_each_term_percents(cls, terms):

        hold = {}
        for term in terms:
            query = {"query": {"match": {"description": f"{term}"}}, "size": 0}
            result = cls.es.es_cli.search(index="job_description", body=query)
            percent = result["hits"]["total"]["value"] / cls.doc_count
            hold[term] = round(percent * 100, 2)
        return hold
