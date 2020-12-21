import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scraper.loaders import JobDescriptionLoader


class GlassdoorSpider(CrawlSpider):
    """
    GlassdoorSpider is a spider inherit from the generic CrawlSpider, and 
    responsible for vacancies scraping on Glassdoor, 
    """

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

    name = "glassdoor"
    allowed_domains = ["www.glassdoor.com"]
    start_urls = __generate_start_urls.__func__(1)
    rules = (
        Rule(
            LinkExtractor(allow=r"glassdoor.com/partner/jobListing.htm"),
            callback="parse_item",
        ),
    )
    xpath_mappings = {
        "title": [
            "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[2]/text()",
            "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[2]/text()",
        ],
        "company": [
            "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[1]/text()",
            "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[1]/text()",
        ],
        "location": [
            "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div[3]/text()",
            "/html/body/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[3]/text()",
        ],
        "description": [
            "/html/body/div[3]/div/div/div[1]/div[3]/div/div/div/div/div",
            "/html/body/div[3]/div/div/div[1]/div[4]/div/div/div/div",
            "/html/body/div[3]/div/div/div[1]/div[3]/div/div/div/div",
        ],
    }

    def parse_item(self, response):
        """
        parse_item is a callback handler for each response of glassdoor job post
        the spider recieved. However, since the target data may locate in more
        than one possible xpath, so we need to loop over all of item with the list
        of possible xpaths until the extract result is not None.
        """
        loader = JobDescriptionLoader(response=response)
        for mapping in self.__class__.xpath_mappings:
            for xpath in self.__class__.xpath_mappings[mapping]:
                loader.add_xpath(mapping, xpath)
                if loader.get_collected_values(mapping):
                    break
        return loader.load_item()
