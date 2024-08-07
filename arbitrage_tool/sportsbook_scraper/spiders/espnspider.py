from typing import Any, Iterable
import scrapy
from scrapy_playwright.page import PageMethod
from sportsbook_scraper.items import SportsbookScraperItem
from scrapy.loader import ItemLoader
from common.helpers import read_yaml
from datetime import datetime
import hashlib
from sportsbook_scraper.spiders.sportsbookspider import SportsbookSpider

class ESPNSpider(SportsbookSpider):
    name = "espnspider"

    def __init__(self, name: str | None = None, sport=None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.sport = sport

    def find_date(self, input_string: str) -> str:
        # Trim any leading or trailing whitespace from the input
        input_string = input_string.strip()

        # Check if the input string is "Today"
        if input_string.lower() == "today":
            return datetime.now().strftime("%Y-%m-%d")

        # Try to parse the input string as a date
        try:
            parsed_date = datetime.strptime(input_string, "%b %d, %Y")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            # If parsing fails, return "LIVE"
            return "LIVE"
        
    def generate_hash_id(self, sideA: str, sideB: str, date: str) -> str:
        # Combine the values into a single string
        combined_string = f"{sideA} vs {sideB} on {date}"
        
        # Generate the SHA-256 hash of the combined string
        hash_object = hashlib.md5(combined_string.encode())
        hash_id = hash_object.hexdigest()
        
        return hash_id
        
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

        date_str = container.xpath(".//div[@class='text-style-xs-medium flex items-center gap-x-2']/span[1]/text()").get()
        date = self.find_date(date_str.split('·')[0])

        sideA = container.xpath(".//div[@class='flex p-0'][1]//div[@class='text-style-s-medium text-primary text-primary']/text()").get()
        sideB = container.xpath(".//div[@class='flex p-0'][2]//div[@class='text-style-s-medium text-primary text-primary']/text()").get()
        gameCode = self.generate_hash_id(sideA, sideB, date)
        
        # Load item and compute game code
        loader.add_value('date', date)
        loader.add_value('gameCode', gameCode)

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
        count = len(response.xpath("//div[@class='text-style-xs-medium flex items-center gap-x-2']/span[1]/text()").getall())
        print(f'\n\n\n\n\n{count}\n\n\n\n\n')
        
        for container in containers:
            if self.sport in read_yaml('sports')['two']:
                pass
            elif self.sport in read_yaml('sports')['two+']:
                yield self.two_parse(container)
            elif self.sport in read_yaml('sports')['three']:
                pass
            else:
                break
