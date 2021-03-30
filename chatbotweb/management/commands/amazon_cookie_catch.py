from django.core.management.base import BaseCommand
from django.utils import timezone
from scrapers.amazon.main import ScraperAmazon
from chatbotweb.models import ScraperCookieCatcher
import json

import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        amazon_domains = '[{"domain":"amazon.co.uk", "zipcode":"SO152GB"},{"domain":"amazon.com", "zipcode":"10004"},{"domain":"amazon.it", "zipcode":"00118"},{"domain":"amazon.fr", "zipcode":"75000"}]';

        amazon_domains = json.loads(amazon_domains)

        for inputData in amazon_domains:
            try:
                data = ScraperAmazon.runBrowser(inputData)
                ScraperCookieCatcher.objects.create(website_domain=inputData['domain'],cookies_data=data,catching_date=datetime.datetime.now())
            except:
                print("Next entry.")

        print("done!")