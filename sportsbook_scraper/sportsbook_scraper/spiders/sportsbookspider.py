from typing import Iterable
import scrapy
from scrapy_playwright.page import PageMethod


class SportsbookspiderSpider(scrapy.Spider):
    name = "sportsbookspider"

    def start_requests(self) -> Iterable[scrapy.Request]:
        url = 'https://sports.oh.betmgm.com/en/sports/football-11/betting/usa-9/nfl-35'
        yield scrapy.Request(
            url=url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'div.event-timer-scoreboard-info'.replace(' ', '.'))
                ]
            )
        )

    async def parse(self, response):
        yield {
            'text': response.text
        }
