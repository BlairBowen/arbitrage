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

    from common.helpers import read_yaml
    from fuzzywuzzy import fuzz

    def find_best_match(sport, input_name):
        best_match = None
        highest_similarity = 0

        if sport in read_yaml('sports')['two']:
            if '.' not in input_name.split(' ')[0]:
                split_name = input_name.split(' ')
                input_name = ' '.join([f'{split_name[0][0]}.', split_name[1]])
            return input_name.lower()
        else:
            config = read_yaml('leagues')[sport]
            # Compare the input name with each name in the list
            for team in config['teams']:
                similarity = fuzz.ratio(input_name, team)
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_match = team

            return best_match.lower()
        
    best_match = find_best_match('boxing', 'J. Jones')
    print(best_match)


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
    main()
