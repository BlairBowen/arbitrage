from arbitrage_tool.arbitrage.classes import Arbitrage, ThreeWayArbitrage
from arbitrage_tool.common.helpers import read_yaml
import scrapy
from scrapy.crawler import CrawlerProcess
from arbitrage_tool.sportsbook_scraper.sportsbook_scraper.spiders.sportsbookspider import SportsbookSpider

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(SportsbookSpider, sport='baseball-mlb')
    process.start()
    pass