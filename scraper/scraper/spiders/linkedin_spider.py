import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.html import replace_tags


class LinkedinSpider(CrawlSpider):

    name = "linkedin"
    allowed_domains = ["linkedin.com"]

    @staticmethod
    def __generate_start_urls(page_count: int = 1):
        """
        generate_start_urls was designed for generating a series of job search
        url of LinkedIn with different slice through \"start\" url parameter.
        """
        if page_count < 1:
            raise ValueError(
                f"generate start_urls failed, page_count must be a integer greater than 0, got {page_count}"
            )

        start_urls = []
        for idx in range(page_count):
            start = int(25 * idx)
            start_urls.append(
                f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?geoId=92000000&keywords=Software%2BEngineer&location=%E5%85%A8%E7%90%83&start={start}"
            )
        return start_urls

    start_urls = __generate_start_urls.__func__(1)
    rules = (
        Rule(LinkExtractor(allow=r"linkedin.com/jobs/view/*"), callback="parse_item"),
    )

    def parse_item(self, response):
        item = {}
        item["title"] = response.xpath(
            "/html/body/main/section[1]/section[2]/div[1]/div[1]/h1/text()"
        ).get()
        item["company"] = response.xpath(
            "/html/body/main/section[1]/section[2]/div[1]/div[1]/h3[1]/span[1]/a/text()"
        ).get()
        item["location"] = response.xpath(
            "/html/body/main/section[1]/section[2]/div[1]/div[1]/h3[1]/span[2]/text()"
        ).get()

        description = response.xpath(
            "/html/body/main/section[1]/section[3]/div/section/div"
        ).extract_first()
        item["description"] = re.sub(
            "( |\n)+", " ", replace_tags(description, " "),
        ).strip()

        yield item
