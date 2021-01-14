import json

from config import AnalyzerLanguagesConfig, AnalyzerDegreesConfig
from analyzer.executor import Executor


class Planner:
    def __init__(self, config):
        self.config = config

    def run(self):
        if self.config["rank_programming_languages"]:
            self.rank_programming_languages()
        if self.config["rank_public_clouds"]:
            self.rank_public_clouds()
        if self.config["rank_degrees"]:
            self.rank_degrees()

    def rank_programming_languages(self):
        result = Executor.get_each_term_percents(
            AnalyzerLanguagesConfig.programming_languages
        )
        print(json.dumps(result, indent=4))

    def rank_public_clouds(self):
        result = Executor.get_each_term_percents(
            AnalyzerLanguagesConfig.public_clouds,
        )
        print(json.dumps(result, indent=4))

    def rank_degrees(self):
        result = {
            "bs_degree": Executor.get_union_percent(
                AnalyzerDegreesConfig.bs_degrees,
            ),
            "ms_degree": Executor.get_union_percent(
                AnalyzerDegreesConfig.ms_degrees,
            ),
        }
        print(json.dumps(result, indent=4))
