import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GlassdoorSpider(CrawlSpider):
    name = "glassdoor"
    allowed_domains = ["www.glassdoor.com"]
    start_urls = [
        "https://www.glassdoor.com/Job/software-engineer-jobs-SRCH_KO0,17.htm?p=1"
    ]

    rules = (
        Rule(
            LinkExtractor(allow=r"/software-engineer-jobs-SRCH_KO0,17.htm\?p=[0-9]"),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        jobs = response.xpath(
            "/html/body/div[3]/div/div/div[1]/div/div[2]/section/article/div[1]/ul/li"
        )
        for jd in jobs:
            item = {}
            item["title"] = jd.xpath("./div[2]/a/span/text()").get()
            item["company"] = jd.xpath("./div[2]/div[1]/a/span/text()").get()
            item["location"] = jd.xpath("./div[2]/div[2]/span/text()").get()
            yield item
