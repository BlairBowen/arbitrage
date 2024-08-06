from typing import Any, Iterable
import scrapy
from scrapy_playwright.page import PageMethod
from sportsbook_scraper.items import SportsbookScraperItem
from scrapy.loader import ItemLoader
from common.helpers import read_yaml


class SportsbookSpider(scrapy.Spider):
    name = "sportsbookspider"

    def __init__(self, name: str | None = None, sport=None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.sport = sport

    def two_parse(self, container):
        loader = ItemLoader(item=SportsbookScraperItem(), selector=container)

        loader.add_xpath('sideA', ".//div[@class='flex p-0'][1]//div[@class='text-style-s-medium text-primary text-primary']")
        loader.add_xpath('sideB', ".//div[@class='flex p-0'][2]//div[@class='text-style-s-medium text-primary text-primary']")
        loader.add_xpath('spread', './/div[@class="flex p-0"][1]//button[@data-dd-action-name="Add Bet Selections"][1]/span[1]')
        loader.add_xpath('spreadA', './/div[@class="flex p-0"][1]//button[@data-dd-action-name="Add Bet Selections"][1]/span[2]')
        loader.add_xpath('spreadB', './/div[@class="flex p-0"][2]//button[@data-dd-action-name="Add Bet Selections"][1]/span[2]')
        loader.add_xpath('total', './/div[@class="flex p-0"][1]//button[@data-dd-action-name="Add Bet Selections"][2]/span[1]')
        loader.add_xpath('over', './/div[@class="flex p-0"][1]//button[@data-dd-action-name="Add Bet Selections"][2]/span[2]')
        loader.add_xpath('under', './/div[@class="flex p-0"][2]//button[@data-dd-action-name="Add Bet Selections"][2]/span[2]')
        loader.add_xpath('moneyA', './/div[@class="flex p-0"][1]//button[@data-dd-action-name="Add Bet Selections"][3]/span[2]')
        loader.add_xpath('moneyB', './/div[@class="flex p-0"][2]//button[@data-dd-action-name="Add Bet Selections"][3]/span[2]')

        print(f'\n\n\n\n\n{loader.load_item()}\n\n\n\n\n')

        return loader.load_item()

    def start_requests(self) -> Iterable[scrapy.Request]:
        url = 'https://espnbet.com/sport/baseball/organization/united-states/competition/mlb'
        yield scrapy.Request(
            url=url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'div.flex flex-col gap-3 rounded p-4 bg-card-primary-temp'.replace(' ', '.'))
                ]
            )
        )

    async def parse(self, response):
        # Iterate through each container with the specific class
        if not self.sport:
            return

        containers = response.xpath('//div[@class="flex flex-col gap-3 rounded p-4 bg-card-primary-temp"]')
        
        for container in containers:
            if self.sport in read_yaml('sports')['two']:
                pass
            elif self.sport in read_yaml('sports')['two+']:
                yield self.two_parse(container)
            elif self.sport in read_yaml('sports')['three']:
                pass
            else:
                break
