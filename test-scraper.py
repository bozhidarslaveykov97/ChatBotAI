from scrapers.amazon.main import ScraperAmazon
import json

amazon_domains = '[{"domain":"amazon.co.uk", "zipcode":"10004"},{"domain":"amazon.com", "zipcode":"10004"},{"domain":"amazon.it", "zipcode":"00118"},{"domain":"amazon.fr", "zipcode":"75000"}]';

amazon_domains = json.loads(amazon_domains)

for inputData in amazon_domains:
    ScraperAmazon.runBrowser(inputData)

print("done!")
