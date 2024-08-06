from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def test():
    import hashlib

    def generate_hash_id(sideA: str, sideB: str, date: str) -> str:
        # Combine the values into a single string
        combined_string = f"{sideA} vs {sideB} on {date}"
        
        # Generate the SHA-256 hash of the combined string
        hash_object = hashlib.md5(combined_string.encode())
        hash_id = hash_object.hexdigest()
        
        return hash_id

    # Example usage
    sideA = 'Arsenal'
    sideB = 'Chelsea'
    date = '2024-08-17'

    hash_id = generate_hash_id(sideA, sideB, date)
    print(hash_id)

def main():
    # Set up the Scrapy project settings
    settings = get_project_settings()

    settings.set('FEEDS', {
        'output.csv': {
            'format': 'csv',
            'overwrite': True  # Overwrite the file if it already exists
        }
    })

    settings.set('ITEM_PIPELINES', {
        'scrapy.pipelines.files.FilesPipeline': 1,
    })

    # Create a CrawlerProcess with the project settings
    process = CrawlerProcess(settings)

    # Specify the spider you want to run
    # Adjust the import path as needed
    from sportsbook_scraper.spiders.sportsbookspider import SportsbookSpider

    # Start the crawling process
    process.crawl(SportsbookSpider, sport='baseball-mlb')
    process.start()

if __name__ == "__main__":
    test()
