# processjobs.py
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import Topic
from ...summarizer import summarize
# import json
class Command(BaseCommand):
    help = 'processes unprocessed jobs'
    
    def handle(self, *args, **kwargs):
        Topics = Topic.objects.filter(summary="")
        for eachTopic in Topics:
            article = eachTopic.scraped_data
            print(article)
            if article != "":
                json = summarize(article)[0]
                summary_text = json['summary_text']
                eachTopic.summary = summary_text
                eachTopic.save()
            else:
                print("""Error: Scrapped Data Not Found
    Description:
    The operation encountered an error because the expected scrapped data is not present. This error typically occurs when attempting to retrieve information from a web page or data source, but the expected content could not be found or fetched.

    Possible Causes:
    1. Invalid URL: The URL provided to fetch the data might be incorrect or inaccessible. Verify that the URL is correct and the web page is reachable.
    2. Data Not Loaded: The scrapped data might not have been loaded or rendered properly due to issues such as slow internet connection, server errors, or JavaScript execution problems.
    3. Changes in Website Structure: Websites often undergo changes in their structure or layout, which can cause the previously defined scraping logic to fail if not updated accordingly.""")
