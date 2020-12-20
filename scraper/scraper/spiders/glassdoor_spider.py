import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scraper.loaders import JobDescriptionLoader


class GlassdoorSpider(CrawlSpider):

    name = "glassdoor"
    allowed_domains = ["www.glassdoor.com"]

    @staticmethod
    def __generate_start_urls(page_count: int = 1):
        """
        generate_start_urls was designed for generating a series of job search
        url of Glassdoor with different slice through \"p\" url parameter.
        """
        if page_count < 1:
            raise ValueError(
                f"generate start_urls failed, page_count must be a integer greater than 0, got {page_count}"
            )

        start_urls = []
        for idx in range(page_count):
            page = idx + 1
            start_urls.append(
                f"https://www.glassdoor.com/Job/software-engineer-jobs-SRCH_KO0,17.htm?p={page}"
            )
        return start_urls

    start_urls = __generate_start_urls.__func__(1)
    rules = (
        Rule(
            LinkExtractor(allow=r"glassdoor.com/partner/jobListing.htm"),
            callback="parse_item",
        ),
    )

    def parse_item(self, response):
        loader = JobDescriptionLoader(response=response)
        loader.add_xpath(
            "title",
            "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[2]/text()",
        )
        if not loader.get_collected_values("title"):
            loader.add_xpath(
                "title",
                "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[2]/text()",
            )

        loader.add_xpath(
            "company",
            "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[1]/text()",
        )
        if not loader.get_collected_values("company"):
            loader.add_xpath(
                "company",
                "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/text()",
            )

        loader.add_xpath(
            "location",
            "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[3]/text()",
        )
        if not loader.get_collected_values("location"):
            loader.add_xpath(
                "location",
                "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[3]/text()",
            )
        
        possible_description_xpaths = [
            "/html/body/div[3]/div/div/div[1]/div[3]/div/div/div/div/div",
            "/html/body/div[3]/div/div/div[1]/div[4]/div/div/div/div",
            "/html/body/div[3]/div/div/div[1]/div[3]/div/div/div/div",
        ]
        for xpath in possible_description_xpaths:
            loader.add_xpath("description", xpath)
            if loader.get_collected_values("description"):
                break

        return loader.load_item()

        """
        item = {}
        item["title"] = response.xpath(
            "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[2]/text()"
        ).get()
        if not item["title"]:
            item["title"] = response.xpath(
                "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[2]/text()"
            ).get()

        item["company"] = response.xpath(
            "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[1]/text()"
        ).get()
        if not item["company"]:
            item["company"] = response.xpath(
                "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/text()"
            ).get()

        item["location"] = response.xpath(
            "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[3]/text()"
        ).get()
        if not item["location"]:
            item["location"] = response.xpath(
                "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[3]/text()"
            ).get()

        description = None
        possible_xpathes = [
            "/html/body/div[3]/div/div/div[1]/div[3]/div/div/div/div/div",
            "/html/body/div[3]/div/div/div[1]/div[4]/div/div/div/div",
            "/html/body/div[3]/div/div/div[1]/div[3]/div/div/div/div",
        ]
        for xpath in possible_xpathes:
            description = response.xpath(xpath).extract_first()
            if description:
                break
        item["description"] = re.sub(
            "( |\n)+", " ", replace_tags(description, " ")
        ).strip()
        yield item
        """
