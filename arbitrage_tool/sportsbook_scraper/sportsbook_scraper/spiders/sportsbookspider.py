from typing import Iterable
import scrapy
from scrapy_playwright.page import PageMethod


class SportsbookspiderSpider(scrapy.Spider):
    name = "sportsbookspider"

    def start_requests(self) -> Iterable[scrapy.Request]:
        # url = 'file:///home/bowenbv/Code/arbitrage_tool/arbitrage_tool/sportsbook_scraper/test.html'
        url = 'https://espnbet.com/sport/football/organization/united-states/competition/nfl'
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
        containers = response.xpath('//div[@class="flex flex-col gap-3 rounded p-4 bg-card-primary-temp"]')
        
        for container in containers:
            # # Extract all text within the current container and its descendants
            # # all_text = container.xpath('.//text()').getall()
            
            # # # Clean up the extracted text
            # # cleaned_text = [text.strip() for text in all_text if text.strip()]
            
            # # yield {'container_text': container.css('div.text-style-s-medium text-primary.text-primary'.replace(' ', '.'))}

            # # buttons = 'button.relative rounded flex h-[48px] flex-1 flex-col items-center justify-center p-1.5 text-style-xs-medium button-bet-selector-deselected'.replace(' ', '.')

            # # elements = container.css('button.relative.rounded.flex.h-[48px].flex-1.flex-col.items-center.justify-center.p-1.5.text-style-xs-medium.button-bet-selector-deselected').getall()
            # elements = container.css('[data-dd-action-name="Add Bet Selections"]')
            # # # yield {'test': [elem.get() for elem in elements]}
            # # yield {'test': elements}

            # # Target elements based on class names (without invalid parts)
            # # elements = response.css('button.relative.rounded.flex.h-[48px].flex-1.flex-col.items-center.justify-center.p-1.5.text-style-xs-medium.button-bet-selector-deselected')
        
            # # for element in elements:
            # #     # Extract text or other attributes as needed
            # #     text = element.css('::text').getall()
            # #     yield {
            # #         'text': text
            # #     }

            # info = [element.css('::text').getall() for element in elements]


            # yield {
            #     'sideA': container.css('div.text-style-s-medium.text-primary.text-primary::text()').getall()[0],
            #     'sideB': container.css('div.text-style-s-medium.text-primary.text-primary::text()').getall()[1],
            #     'spread': info[0][1:],
            #     'spreadA': info[1],
            #     'spreadB': info[6],
            #     'total': info[2].split(' ')[-1],
            #     'over': info[3],
            #     'under': info[8],
            #     'moneyA': info[4],
            #     'moneyB': info[9],
            # }

            # sideA = container.xpath('.//div[contains(@class, "text-style-s-medium") and contains(@class, "text-primary")][1]//text()').get()
            # sideB = container.xpath('.//div[contains(@class, "text-style-s-medium") and contains(@class, "text-primary")][2]//text()').get()

            # sideA = container.css('div.text-style-s-medium.text-primary.text-primary::text()').getall()[0]
            # sideB = container.css('div.text-style-s-medium.text-primary.text-primary::text()').getall()[1]

            # Extract elements with a specific attribute
            info = container.xpath('.//button[@data-dd-action-name="Add Bet Selections"]')
            # info = container.xpath('.//button[@data-dd-action-name="Add Bet Selections"]').getall()
            # info = container.xpath('.//button[@data-dd-action-name="Add Bet Selections"]//text()').getall()

            yield {
                'sideA': container.css('div.text-style-s-medium.text-primary.text-primary::text').getall()[0],
                'sideB': container.css('div.text-style-s-medium.text-primary.text-primary::text').getall()[1],
                'spread': info[0].css('span::text').getall()[0][1:],
                'spreadA': info[0].css('span::text').getall()[1],
                'spreadB': info[3].css('span::text').getall()[1],
                'total': info[1].css('span::text').getall()[0].split(' ')[-1],
                'over': info[1].css('span::text').getall()[1],
                'under': info[4].css('span::text').getall()[1],
                'moneyA': info[2].css('span::text').getall()[0],
                'moneyB': info[5].css('span::text').getall()[0],
            }

            
            # yield {
            #     'sideA': container.css('div.text-style-s-medium.text-primary.text-primary::text').getall()[0],
            #     'sideB': container.css('div.text-style-s-medium.text-primary.text-primary::text').getall()[1],
            #     'spread': info[0][1:],
            #     'spreadA': info[1],
            #     'spreadB': info[6],
            #     'total': info[2].split(' ')[-1],
            #     'over': info[3],
            #     'under': info[8],
            #     'moneyA': info[4],
            #     'moneyB': info[9],
            # }

        # # Target specific container
        # containers = response.xpath('//div[@class="flex flex-col gap-3 rounded p-4 bg-card-primary-temp"]')
        
        # for container in containers:
        #     # Extract all text within the current container
        #     all_text = container.xpath('.//text()').getall()
            
        #     # Clean up the extracted text
        #     cleaned_text = ' '.join([text.strip() for text in all_text if text.strip()])
            
        #     # Extract text using corrected CSS selector
        #     elements = container.css('div.text-style-s-medium.text-primary.text-primary span::text').get()
        #     yield {'container_text': cleaned_text, 'elements_text': elements}
                