# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


class SportsbookScraperItem(scrapy.Item):
    # define the fields for your item here like:
    sideA = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    sideB = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    spread = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    spreadA = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    spreadB = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    total = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    over = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    under = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    moneyA = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    moneyB = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    moneyC = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())