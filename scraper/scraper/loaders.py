import re
from w3lib.html import replace_tags
from itemloaders.processors import TakeFirst, Compose
from scrapy.loader import ItemLoader

from scraper.items import JobDescriptionItem


class JobDescriptionLoader(ItemLoader):
    """
    JobDescriptionLoader is the loader with pre-defined output
    processor for JobDescription item.
    """

    @staticmethod
    def __flatten(digest):
        return re.sub(
            "( | |\n|\r|\t)+",
            " ",
            replace_tags(digest, " "),
        ).strip()

    __standardize = Compose(TakeFirst(), lambda x: x.strip())
    __standardize_description = Compose(TakeFirst(), __flatten.__func__)

    default_item_class = JobDescriptionItem
    title_out = __standardize
    company_out = __standardize
    location_out = __standardize
    description_out = __standardize_description
