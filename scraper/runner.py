from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.linkedin_spider import LinkedinSpider
from scraper.spiders.glassdoor_spider import GlassdoorSpider


class Runner:
    """
    Runner is a mediator to drive all scraper execution.
    """

    def __init__(self):
        self.process = CrawlerProcess(get_project_settings())
        self.spiders = [LinkedinSpider, GlassdoorSpider]

    def run_all(self):
        for spider in self.spiders:
            self.process.crawl(spider)
        self.process.start()
